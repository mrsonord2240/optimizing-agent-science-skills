#!/usr/bin/env python
"""NEW INPUT 8: the consensus-mode documentation the fixer rewrote (--het-fract / --call-fract / --ambig / --het-scale / -d / -a / -aa / -T and the
bcftools consensus IUPAC note), judged on MY OWN fixture (seed 11, transitions as the minor allele, depths 20 and 60, fractions 50..5 %),
predictions computed independently in Python before comparing with samtools 1.24 / bcftools 1.24 output."""
import itertools, os, random, shutil, sys
sys.path.insert(0, '/mnt/openscience/audits/bio-reference-operations/run')
from auditlib import *
import pysam
D = f'{W}/work/r8'; shutil.rmtree(D, ignore_errors=True); os.makedirs(D)
random.seed(11)
L = 2000
ref = [random.choice('ACGT') for _ in range(L)]
trans = {'A': 'G', 'G': 'A', 'C': 'T', 'T': 'C'}
IUP = {frozenset('AG'): 'R', frozenset('CT'): 'Y'}
fr = [(50, 0.5), (0.4,), ]
cols = []                       # (position 0-based, depth, n_minor)
fractions = [0.5, 0.4, 0.3, 0.25, 0.2, 0.15, 0.1, 0.05]
for di, depth in enumerate((20, 60)):
    for fi, f in enumerate(fractions):
        pos = 100 + 100 * (di * len(fractions) + fi)
        cols.append((pos, depth, round(f * depth)))
ref_s = ''.join(ref)
# make the last 100 bp block (1900-1999) covered; gap 1650..1899 is soft-masked in the FASTA and uncovered
with open(f'{D}/g.fa', 'w') as f:
    f.write('>g\n')
    s = ref_s[:1650] + ref_s[1650:1900].lower() + ref_s[1900:]
    f.write('\n'.join(s[i:i + 60] for i in range(0, L, 60)) + '\n')
hdr = {'HD': {'VN': '1.6', 'SO': 'coordinate'}, 'SQ': [{'SN': 'g', 'LN': L}]}
reads = []
for pos, depth, nm in cols:
    for k in range(depth):
        st = pos - 30 - (k % 5)                                  # 60 bp reads, column inside every read
        seq = list(ref_s[st:st + 60]); seq[pos - st] = trans[ref[pos]] if k < nm else ref[pos]
        reads.append((st, ''.join(seq), 'c%d_%d' % (pos, k)))
for k in range(5):                                               # block 1900..1999 depth 5, reference-identical
    reads.append((1900 + k, ref_s[1900 + k:1960 + k], 'tail%d' % k))
    reads.append((1940 - k, ref_s[1940 - k:2000 - k], 'tailb%d' % k))
reads.sort()
with pysam.AlignmentFile(f'{D}/g.bam', 'wb', header=hdr) as out:
    for st, seq, name in reads:
        a = pysam.AlignedSegment(out.header); a.query_name = name; a.query_sequence = seq; a.flag = 0; a.reference_id = 0; a.reference_start = st
        a.mapping_quality = 60; a.cigartuples = [(0, len(seq))]; a.query_qualities = pysam.qualitystring_to_array('I' * len(seq)); out.write(a)
pysam.index(f'{D}/g.bam')
print('columns (pos1, depth, minor reads):', [(p + 1, d, n) for p, d, n in cols][:4], '... n =', len(cols))

def cons(args, pad=True):
    # -a is added so that string index == 0-based reference position (the SKILL's own recipe for aligned coordinates); pad=False for the -a tests
    rc, o, e = sh(f'samtools consensus {"-a " if pad else ""}{args} g.bam', D)
    s = ''.join(l for l in o.splitlines() if not l.startswith('>')); return s, e
def at(s): return [s[p] for p, d, n in cols]
def pred_simple(h, c, ambig):
    out = []
    for p, d, n in cols:
        a, b = d - n, n                                          # major, minor counts (minor <= major here)
        if a == b: top, sec = a, b
        else: top, sec = max(a, b), min(a, b)
        maj = ref[p] if a >= b else trans[ref[p]]
        if b == 0: out.append(maj)
        elif ambig and sec / top >= h: out.append(IUP[frozenset((ref[p], trans[ref[p]]))])
        elif top / d >= c: out.append(maj)
        else: out.append('N')
    return out
print('reference bases at the 16 columns:', [ref[p] for p, d, n in cols])
print('depth 20 columns then depth 60 columns; minor fraction 0.5,0.4,0.3,0.25,0.2,0.15,0.1,0.05 in each')

print('##### -m simple: predicted vs observed on the grid of (het-fract, call-fract, --ambig)')
allok = True; rows = []
for h, c, amb in itertools.product((0.05, 0.15, 0.3, 0.6), (0.5, 0.75, 0.9), (True, False)):
    obs = at(cons(f'-m simple --het-fract {h} --call-fract {c} {"--ambig" if amb else ""} -d 1')[0])
    exp = pred_simple(h, c, amb)
    ok = all(o == e or (cols[i][2] * 2 == cols[i][1] and e in (ref[cols[i][0]], trans[ref[cols[i][0]]]) and o in (ref[cols[i][0]], trans[ref[cols[i][0]]])) for i, (o, e) in enumerate(zip(obs, exp))); allok &= ok   # 50/50 columns: either base is a valid tie-break
    if not ok: rows.append((h, c, amb, ''.join(obs), ''.join(exp)))
check('simple mode rule (IUPAC iff --ambig and minor/major >= het-fract; else base iff major/depth >= call-fract; else N) predicts all 48 grid outputs x 16 columns', allok, rows[:3])
def rule(h, c, amb): return ''.join(at(cons(f'-m simple --het-fract {h} --call-fract {c} {"--ambig" if amb else ""} -d 1')[0]))
print('    sample outputs (16 columns: d20 fractions .5 .4 .3 .25 .2 .15 .1 .05 | d60 same):')
for h, c, amb in ((0.15, 0.75, True), (0.3, 0.75, True), (0.15, 0.9, False), (0.15, 0.6, False)):
    print('    het-fract %-4s call-fract %-4s ambig %-5s' % (h, c, amb), rule(h, c, amb))
# default (flag omitted)
om = ''.join(at(cons('-m simple --ambig -d 1')[0])); om15 = ''.join(at(cons('-m simple --ambig --het-fract 0.15 -d 1')[0]))
print('    simple --ambig, het-fract OMITTED  :', om); print('    simple --ambig, --het-fract 0.15   :', om15)
check('SKILL: with --het-fract omitted the 15% minor column stays a plain base although --help prints 0.15 (omitted != 0.15 output)', om != om15 and om[5] not in 'RY' and om15[5] in 'RY', (om[5], om15[5]))
# what threshold does the omitted default behave like?
eq = [h for h in (0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0) if ''.join(at(cons(f'-m simple --ambig --het-fract {h} -d 1')[0])) == om]
print('    omitted --het-fract behaves like explicit --het-fract in', eq)
# call-fract default
cd = ''.join(at(cons('-m simple -d 1')[0])); c75 = ''.join(at(cons('-m simple --call-fract 0.75 -d 1')[0]))
check('SKILL/--help: --call-fract default is 0.75 (omitted == explicit 0.75)', cd == c75, (cd, c75))
print('    simple (defaults, no --ambig):', cd)

print('##### default Bayesian mode: flags are ignored; --ambig required for IUPAC; --het-scale is the knob')
b0 = cons('-d 1')[0]
same = all(cons(f'-d 1 {x}')[0] == b0 for x in ('--het-fract 0.05', '--het-fract 0.9', '--call-fract 0.95', '--call-fract 0.1', '--het-fract 0.2 --call-fract 0.5'))
check('SKILL: --het-fract / --call-fract change nothing in the default Bayesian mode (byte-identical, whole contig)', same)
ba = cons('-d 1 --ambig')[0]
print('    Bayesian default        :', ''.join(at(b0))); print('    Bayesian --ambig        :', ''.join(at(ba)))
check('SKILL: without --ambig no IUPAC letter appears anywhere in the Bayesian output', not set(b0) & set('RYSWKMBDHV'), sorted(set(b0)))
iup_cols = [i for i, ch in enumerate(at(ba)) if ch in 'RY']
nn = [i for i, ch in enumerate(at(b0)) if ch == 'N']
check('SKILL: a column that becomes IUPAC with --ambig is N without it (%d ambiguous columns)' % len(iup_cols), iup_cols and all(at(b0)[i] == 'N' for i in iup_cols), (iup_cols, nn))
bs1 = ''.join(at(cons('-d 1 --ambig --het-scale 0.01')[0])); bs2 = ''.join(at(cons('-d 1 --ambig --het-scale 100')[0]))
print('    Bayesian --ambig --het-scale 0.01:', bs1); print('    Bayesian --ambig --het-scale 100 :', bs2)
n_iup = lambda s: sum(1 for ch in s if ch in 'RY')
check('SKILL: --het-scale < 1 gives fewer IUPAC calls, > 1 more (0.01: %d, 1: %d, 100: %d)' % (n_iup(bs1), n_iup(''.join(at(ba))), n_iup(bs2)), n_iup(bs1) <= n_iup(''.join(at(ba))) <= n_iup(bs2) and n_iup(bs1) < n_iup(bs2), (n_iup(bs1), n_iup(''.join(at(ba))), n_iup(bs2)))
check('-A is the short form of --ambig', cons('-d 1 -A')[0] == ba)
print('    the 15% column (index 5 / 13) Bayesian default:', at(b0)[5], at(b0)[13], '; the 5% column:', at(b0)[7], at(b0)[15], '(the 50% col at depth 20/60:', at(b0)[0], at(b0)[8], ')')

print('##### -d')
o30 = at(cons('-d 30 --ambig')[0])
check('SKILL -d N (Bayesian --ambig): the 8 depth-20 columns (< 30) are N, the 8 depth-60 columns are called', all(ch == 'N' for ch in o30[:8]) and all(ch != 'N' for ch in o30[8:]), ''.join(o30))
o30s = at(cons('-m simple --call-fract 0.5 -d 30')[0]); check('SKILL -d N in -m simple mode too', all(ch == 'N' for ch in o30s[:8]) and all(ch != 'N' for ch in o30s[8:]), ''.join(o30s))
o1s = at(cons('-m simple --call-fract 0.5 -d 1')[0]); check('same columns at -d 1 are called (so N above came from -d, not from ambiguity)', all(ch != 'N' for ch in o1s), ''.join(o1s))

print('##### -a / -aa / -T on this contig (reads cover 30..1649 and 1900..1999; contig 2000 bp; 1650..1899 uncovered and soft-masked)')
sd = cons('-d 1', False)[0]; sa = cons('-d 1 -a', False)[0]; saa = cons('-d 1 -aa', False)[0]
print('    lengths default / -a / -aa:', len(sd), len(sa), len(saa), '| default starts', sd[:6], 'ends', sd[-6:], '| -a starts', sa[:6])
check('-a pads the contig ends with N to the header LN (2000); default output spans only the called region; -aa == -a for a contig that has reads', len(sa) == 2000 and len(sd) < 2000 and sa.startswith('N') and saa == sa, (len(sd), len(sa), len(saa)))
check('calls inside the covered span are identical with and without -a', sa.strip('N') == sd.strip('N') or sd in sa, (len(sd), len(sa)))
st = cons('-d 1 -a -T g.fa', False)[0]
gap = st[1650:1900]
check('SKILL -T: the uncovered soft-masked gap 1650..1899 is filled with the reference bases IN THE FASTA CASE (lower-case)', gap == ref_s[1650:1900].lower(), gap[:20])
check('SKILL -T: covered columns keep their normal (upper-case) call', st[100:130] == sa[100:130] and st[100:130].isupper())
print('##### FASTQ')
rc, o, e = sh('samtools consensus -f fastq -l 0 g.bam', D); ln = o.splitlines()
check('SKILL: -f fastq -l 0 -> 4 lines per record (unwrapped)', len(ln) == 4 and ln[0].startswith('@') and ln[2] == '+', len(ln))
rc, o, e = sh('samtools consensus -f fastq g.bam', D); check('SKILL: FASTQ wrapped at 70 columns by default (more than 4 lines)', len(o.splitlines()) > 4 and max(len(x) for x in o.splitlines()) <= 70, len(o.splitlines()))

print('##### bcftools consensus IUPAC note (own VCF on the same reference)')
vcf = ['##fileformat=VCFv4.2', '##contig=<ID=g,length=%d>' % L, '##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">', '#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tS1']
P = {'unph': 200, 'ph01': 300, 'ph10': 400, 'hom': 500}
vcf.append('g\t%d\t.\t%s\t%s\t50\tPASS\t.\tGT\t0/1' % (P['unph'] + 1, ref[P['unph']], trans[ref[P['unph']]]))
vcf.append('g\t%d\t.\t%s\t%s\t50\tPASS\t.\tGT\t0|1' % (P['ph01'] + 1, ref[P['ph01']], trans[ref[P['ph01']]]))
vcf.append('g\t%d\t.\t%s\t%s\t50\tPASS\t.\tGT\t1|0' % (P['ph10'] + 1, ref[P['ph10']], trans[ref[P['ph10']]]))
vcf.append('g\t%d\t.\t%s\t%s\t50\tPASS\t.\tGT\t1/1' % (P['hom'] + 1, ref[P['hom']], trans[ref[P['hom']]]))
open(f'{D}/v.vcf', 'w', newline='\n').write('\n'.join(vcf) + '\n')
sh('bgzip -f v.vcf; tabix -f -p vcf v.vcf.gz', D)
def bc_(args):
    rc, o, e = sh(f'bcftools consensus -f g.fa {args} v.vcf.gz', D)
    s = ''.join(l for l in o.splitlines() if not l.startswith('>')).upper(); return s, rc, e
alt = {k: trans[ref[p]] for k, p in P.items()}; rf = {k: ref[p] for k, p in P.items()}
iu = {k: IUP[frozenset((rf[k], alt[k]))] for k in P}
s, rc, e = bc_('')
print('    default:', [s[P[k]] for k in P], 'expected IUPAC/IUPAC/IUPAC/ALT =', [iu['unph'], iu['ph01'], iu['ph10'], alt['hom']], e.strip()[:80])
check('SKILL: no -H, GT genotypes: heterozygous SNPs become IUPAC (unphased 0/1, phased 0|1 and 1|0), hom-alt stays ALT', [s[P[k]] for k in P] == [iu['unph'], iu['ph01'], iu['ph10'], alt['hom']], [s[P[k]] for k in P])
s1, _, _ = bc_('-H 1'); s2, _, _ = bc_('-H 2'); sA, _, _ = bc_('-H A'); sm, _, e3 = bc_('-s -')
print('    -H 1:', [s1[P[k]] for k in P], '-H 2:', [s2[P[k]] for k in P], '-H A:', [sA[P[k]] for k in P], '-s -:', [sm[P[k]] for k in P], e3.strip()[:100])
check('SKILL: -H 1 / -H 2 pick one haplotype of the phased hets (0|1 -> REF/ALT, 1|0 -> ALT/REF)', s1[P['ph01']] == rf['ph01'] and s1[P['ph10']] == alt['ph10'] and s2[P['ph01']] == alt['ph01'] and s2[P['ph10']] == rf['ph10'] and s1[P['hom']] == alt['hom'], (s1[P['ph01']], s1[P['ph10']], s2[P['ph01']], s2[P['ph10']]))
check('SKILL: -H A applies every ALT allele (het columns -> ALT)', all(sA[P[k]] == alt[k] for k in P), [sA[P[k]] for k in P])
check('SKILL: -s - also applies every ALT allele', all(sm[P[k]] == alt[k] for k in P), [sm[P[k]] for k in P])
summary()
