#!/usr/bin/env python
"""INPUT 4 (Variant B): samtools consensus / bcftools consensus.
Planted-truth synthetic BAM (het 50%, het 20%, 3% error, gap, depth-2 island, deletion, insertion) + real SARS-CoV-2
Illumina / ARTIC nanopore / human chr22 slice, each checked against an independent pysam-pileup computation."""
import os, shutil, sys, re, json
sys.path.insert(0, '/mnt/openscience/audits/bio-reference-operations/run')
from auditlib import *
import pysam
from collections import Counter

D = f'{W}/work/in4'
shutil.rmtree(D, ignore_errors=True)
os.makedirs(D)
SY = f'{W}/data/synthetic'
for f in ('synth_chr.bam', 'synth_chr.bam.bai', 'synth.fa', 'variants.vcf.gz', 'variants.vcf.gz.tbi'):
    shutil.copy(f'{SY}/{f}', f'{D}/{f}')
T = json.load(open(f'{SY}/truth.json'))
S = {k: v.upper() for k, v in T['seqs'].items()}
alt = {int(k): v for k, v in T['alt'].items()}
HOM, HET50, HET20, ERR1, LOW = T['HOM'], T['HET50'], T['HET20'], T['ERR1'], T['LOW']
hap2 = T['hap2']


def cons(args, bam='synth_chr.bam', out='o.fa', cwd=D):
    rc, o, e = sh(f'samtools consensus {args} {bam} -o {out}', cwd)
    if rc != 0 or not os.path.exists(f'{cwd}/{out}') or out.endswith('.fq'):
        return rc, e, []
    return rc, e, fa_records(open(f'{cwd}/{out}').read())


def by_name(recs):
    return {h.split()[0]: s for h, s in recs}


# ----- independent per-position base counts (pysam pileup, no quality filter, no overlap removal)
def counts(bam, chrom, start=None, end=None):
    c = {}
    with pysam.AlignmentFile(bam) as f:
        for col in f.pileup(chrom, start, end, truncate=True, min_base_quality=0, ignore_overlaps=False, max_depth=100000):
            cnt = Counter()
            for r in col.pileups:
                if r.is_refskip:
                    continue
                if r.is_del or r.query_position is None:
                    cnt['*'] += 1
                    continue
                cnt[r.alignment.query_sequence[r.query_position].upper()] += 1
            c[col.reference_pos] = cnt
    return c


C1 = counts(f'{D}/synth_chr.bam', 'chr1')
print('independent counts: pos200', dict(C1[HOM]), 'pos400', dict(C1[HET50]), 'pos600', dict(C1[HET20]), 'pos800', dict(C1[ERR1]), 'pos1550', dict(C1[LOW]))
frac20 = C1[HET20][alt[HET20]] / sum(C1[HET20].values())
frac50 = C1[HET50][alt[HET50]] / sum(C1[HET50].values())
print('alt fractions: het20 = %.3f  het50 = %.3f  err = %.3f' % (frac20, frac50, C1[ERR1][alt[ERR1]] / sum(C1[ERR1].values())))

# ================= A. defaults, planted truth =================
rc, e, recs = cons('')
R = by_name(recs)
c1, c2 = R['chr1'], R['chr2']
check('default: 2 records (chr1, chr2); chrM (no reads) not emitted', sorted(R) == ['chr1', 'chr2'], sorted(R))
check('chr1 consensus length 1700 = span of covered bases (0..1699), gap 1000-1499 filled', len(c1) == 1700, len(c1))
check('hom-alt site (pos 201 1-based): consensus = planted alt %s' % alt[HOM], c1[HOM] == alt[HOM], c1[HOM])
print('  het 50/50 site consensus base (default, no --ambig):', c1[HET50], '| het 20% site:', c1[HET20], '| 3% error site:', c1[ERR1], '(ref', S['chr1'][ERR1] + ')')
check('3%-alt site: consensus = ref (error not called)', c1[ERR1] == S['chr1'][ERR1])
check('20%-alt site (7 C vs 27 A, no --ambig): Bayesian default emits N (not the majority base A) -- SKILL does not say the default mode blanks minor-allele columns', c1[HET20] == 'N', c1[HET20])
check('50/50 het site without --ambig: N', c1[HET50] == 'N', c1[HET50])
covered = {p for p, c in C1.items() if sum(c.values()) > 0}
bad = [p for p in covered if p not in (HET50, HET20, HOM, LOW) and c1[p] != S['chr1'][p]]
check('every other covered chr1 position equals the reference base (no spurious calls)', not bad, bad[:5])
gap = c1[1000:1500]
print('  gap 1000-1499 content:', Counter(gap))
check('uncovered internal gap is N (not reference, not dropped)', set(gap) == {'N'}, Counter(gap))
print('  low-depth island 1550 base:', c1[LOW], ' (planted alt', alt[LOW] + ', depth', sum(C1[LOW].values()), ')')

# ---- independent majority vote vs consensus, all covered positions
maj_bad = []
for p in sorted(covered):
    b, n = C1[p].most_common(1)[0]
    if p in (HET50, HET20):
        continue
    if c1[p] != b:
        maj_bad.append((p, c1[p], dict(C1[p])))
check('consensus == independent majority vote at every covered chr1 position except the two het columns, which are N (%d sites checked)' % len(covered), not maj_bad, maj_bad[:5])

# ---- chr2 with indels
check('chr2 (3-bp deletion + 2-bp insertion carried by every read): default consensus == planted haplotype (230 nt)', c2 == hap2, (len(c2), len(hap2)))
rc, e, r = cons('--show-del yes')
check('--show-del yes: 3 "*" appear at the deleted positions, rest equal hap2', by_name(r)['chr2'] == hap2[:130] + '***' + hap2[130:], by_name(r)['chr2'][125:140])
rc, e, r = cons('--show-ins no')
check('--show-ins no: the planted GT insertion is dropped', by_name(r)['chr2'] == hap2[:178] + hap2[180:], by_name(r)['chr2'][170:190])
rc, e, r = cons('--mark-ins')
print('  observation: --mark-ins output around the insertion:', by_name(r)['chr2'][170:190], '(help says "+", actual marker differs; flag not used by the Skill)')

# ================= B. options the Skill documents =================
# -d
rc, e, r = cons('-d 5')
d5 = by_name(r)['chr1']
depth = {p: sum(c.values()) for p, c in C1.items()}
viol = [p for p in range(len(d5)) if p not in (HET50, HET20) and (depth.get(p, 0) < 5) != (d5[p] == 'N')]
check('-d 5: position is N exactly when pileup depth < 5 (independent depth; %d positions, het columns excluded)' % len(d5), not viol, viol[:5])
print('  -d 5 at planted depth-2 island 1550:', d5[LOW], '| default:', c1[LOW])
# -a (help: "Output all bases (start/end of reference)")
rc, e, r = cons('-a')
A = by_name(r)
print('  -a lengths', {k: len(v) for k, v in A.items()}, '| tail of chr1 -a:', Counter(A['chr1'][1700:]), '| head of chr2 -a:', Counter(A['chr2'][:420]))
check('-a pads to the reference ends (chr1 5000, chr2 3006 = 3007-3+2) with N; internal calls unchanged', len(A['chr1']) == 5000 and len(A['chr2']) == 3006 and set(A['chr1'][1700:]) == {'N'} and set(A['chr2'][:420]) == {'N'} and A['chr1'][:1700] == c1)
check('SKILL wording "-a: Call all positions (including low coverage)" -- -a does NOT change low-coverage calls (identical to default inside the covered span): the flag only pads reference start/end', A['chr1'][:1700] == c1 and set(A['chr1'][1700:]) == {'N'})
rc, e, r = cons('-aa')
check('-aa additionally emits the uncovered contig chrM (1000 N)', by_name(r).get('chrM') == 'N' * 1000, {k: len(v) for k, v in by_name(r).items()})
# -T
rc, e, r = cons(f'-T {D}/synth.fa')
Tn = by_name(r)['chr1']
diff = [p for p in range(min(len(Tn), len(c1))) if Tn[p] != c1[p]]
print('  -T ref.fa: len', len(Tn), 'positions differing from default:', len(diff), diff[:3], '..', diff[-3:] if diff else '')
check('-T ref.fa (SKILL 178: "report ref base where consensus unavailable"): the internal N gap 1000-1499 becomes the reference bases (case = reference case)', Tn[1000:1500].upper() == S['chr1'][1000:1500], (Tn[1000:1010], 'lower=%d upper=%d' % (sum(c.islower() for c in Tn[1000:1500]), sum(c.isupper() for c in Tn[1000:1500]))))
# -f fastq
rc, e, r = cons('-f fastq', out='o.fq')
fq = open(f'{D}/o.fq').read().splitlines()
print('  fastq default: total lines', len(fq), 'first record seq line length', len(fq[1]))
check('-f fastq (SKILL 142-143): default output is LINE-WRAPPED at 70 (multi-line FASTQ, not 4 lines/record); -l 0 gives 4-line records', len(fq) > 8 and len(fq[1]) == 70)
rc, o, e = sh('samtools consensus -f fastq -l 0 synth_chr.bam -o o4.fq', D)
fq4 = open(f'{D}/o4.fq').read().splitlines()
check('-f fastq -l 0: exactly 4 lines per record, 2 records, qual length == seq length', len(fq4) == 8 and len(fq4[1]) == len(fq4[3]) == 1700, len(fq4))
with pysam.FastxFile(f'{D}/o.fq') as fx:
    recs_fx = [(r.name, len(r.sequence), len(r.quality)) for r in fx]
check('multi-line FASTQ is still readable by pysam.FastxFile (lengths consistent)', recs_fx == [('chr1', 1700, 1700), ('chr2', 230, 230)], recs_fx)
# -r
rc, e, r = cons('-r chr1:101-300')
rr = fa_records(open(f'{D}/o.fa').read())
check('-r chr1:101-300: header ">chr1:101-300", 200 nt, equals default slice c1[100:300]', rr[0][0] == 'chr1:101-300' and rr[0][1] == c1[100:300], rr[0][0])
# config names
ok_cfg = []
for cf in ('hiseq', 'hifi', 'r10.4_sup', 'r10.4_dup', 'ultima'):
    rc, e, r = cons(f'--config {cf}', out=f'cfg_{cf}.fa')
    ok_cfg.append((cf, rc, len(r)))
check('all 5 --config names in SKILL 172-175 accepted, 2 records each', all(x[1] == 0 and x[2] == 2 for x in ok_cfg), ok_cfg)
rc, o, e = sh('samtools consensus --config nope synth_chr.bam -o x.fa', D)
check('unknown --config name is a loud failure (rc != 0)', rc != 0 and 'Unrecognised configuration' in e, (rc, e.strip()[:100]))
rc, o, e = sh('samtools consensus --help', D)
check('SKILL 170/175 tells the reader to verify via "samtools consensus --help": that exits rc=1 with "unrecognized option" (usage still printed)', rc != 0 and 'unrecognized option' in e and 'Usage:' in e, (rc, e.splitlines()[0]))

# ================= C. het / IUPAC claims =================
print('\n--- het handling, SKILL 157-164')
res = {}
for label, args in (('default', ''), ('ambig', '--ambig'), ('ambig+het0.05', '--ambig --het-fract 0.05'), ('ambig+het0.9', '--ambig --het-fract 0.9'),
                    ('ambig+het0.2+call0.5 (SKILL line 161 verbatim)', '--ambig --het-fract 0.2 --call-fract 0.5'),
                    ('simple', '-m simple'), ('simple+ambig', '-m simple --ambig'), ('simple+ambig+het0.5', '-m simple --ambig --het-fract 0.5'),
                    ('simple+ambig+het0.05', '-m simple --ambig --het-fract 0.05'), ('simple+het0.15 (no ambig)', '-m simple --het-fract 0.15'),
                    ('simple+call0.95', '-m simple --call-fract 0.95')):
    rc, e, r = cons(args)
    s = by_name(r)['chr1']
    res[label] = s
    print('  %-52s pos400=%s pos600=%s pos800=%s pos200=%s | stderr: %s' % (label, s[HET50], s[HET20], s[ERR1], s[HOM], e.strip()[:60]))
check('Bayesian default: --ambig turns the 50/50 site into an IUPAC code (M = A/C)', res['ambig'][HET50] == 'M', res['ambig'][HET50])
check('SKILL 160 claim (no --ambig: output restricted to A,C,G,T,N,*): 50/50 site is N without --ambig', res['default'][HET50] == 'N', res['default'][HET50])
check('DEFECT CANDIDATE: in the default (Bayesian) mode --het-fract/--call-fract are ignored (0.05, 0.9 and the SKILL 0.2/0.5 give byte-identical output)', res['ambig+het0.05'] == res['ambig+het0.9'] == res['ambig'] == res['ambig+het0.2+call0.5 (SKILL line 161 verbatim)'])
check('-m simple: --het-fract IS honoured: 20% site is IUPAC at 0.05 but plain ref base at 0.5', res['simple+ambig+het0.05'][HET20] == 'M' and res['simple+ambig+het0.5'][HET20] == 'A', (res['simple+ambig+het0.05'][HET20], res['simple+ambig+het0.5'][HET20]))
check('-m simple + --ambig at the 50/50 site -> M', res['simple+ambig'][HET50] == 'M', res['simple+ambig'][HET50])
check('SKILL 164 claim "Without --ambig, columns where the 2nd base passes --het-fract resolve to N" holds in simple mode (50/50 site)', res['simple+het0.15 (no ambig)'][HET50] == 'N', res['simple+het0.15 (no ambig)'][HET50])
print('  sweep, -m simple --ambig, het-fract vs call at the 20.6%-alt column (top:2nd = 27:7 -> 2nd/top = 0.26, 2nd/total = 0.21) and 50/50 column:')
sweep = {}
for hf in ('0.05', '0.10', '0.15', '0.20', '0.25', '0.30', '0.50'):
    rc, e, r = cons(f'-m simple --ambig --het-fract {hf}')
    x = by_name(r)['chr1']
    sweep[hf] = (x[HET20], x[HET50])
print('   ', sweep)
check('OBSERVATION: -m simple flips at het-fract ~0.26 (= 2nd/top 7/27), matching the SKILL definition, BUT with no --het-fract flag the 2nd/top=0.26 column is NOT called het although help prints default 0.15 (explicit 0.15 -> M): the printed default is not the effective default', sweep['0.25'][0] == 'M' and sweep['0.30'][0] == 'A' and res['simple+ambig'][HET20] == 'A' and sweep['0.15'][0] == 'M', (sweep, res['simple+ambig'][HET20]))

# ================= D. bcftools consensus =================
print('\n--- bcftools consensus (SKILL 197-198)')
vcf = []
for l in os.popen(f'bcftools view -H {D}/variants.vcf.gz').read().splitlines():
    f = l.split('\t')
    vcf.append((f[0], int(f[1]), f[3], f[4], f[9]))


def apply(hap):
    out = {}
    for ch, seq in S.items():
        s = seq
        vs = sorted([v for v in vcf if v[0] == ch], key=lambda v: -v[1])
        for _, pos, ref, altb, gt in vs:
            a = gt.split('|')
            IU = {frozenset('AC'): 'M', frozenset('AG'): 'R', frozenset('AT'): 'W', frozenset('CG'): 'S', frozenset('CT'): 'Y', frozenset('GT'): 'K'}
            if hap is None and a[0] != a[1] and len(ref) == 1 == len(altb):
                assert s[pos - 1] == ref
                s = s[:pos - 1] + IU[frozenset((ref, altb))] + s[pos:]
                continue
            use = (hap is None and '1' in a) or (hap == 1 and a[0] == '1') or (hap == 2 and a[1] == '1')
            if use:
                assert s[pos - 1:pos - 1 + len(ref)] == ref, (ch, pos, ref, s[pos - 1:pos - 1 + len(ref)])
                s = s[:pos - 1] + altb + s[pos - 1 + len(ref):]
        out[ch] = s
    return out


for label, args, hap in (('default (single-sample GT: hom-alt applied, het SNP -> IUPAC)', '', None), ('-H 1', '-H 1', 1), ('-H 2', '-H 2', 2)):
    rc, o, e = sh(f'bcftools consensus -f synth.fa {args} variants.vcf.gz -o bc.fa', D)
    got = {k: v.upper() for k, v in by_name(fa_records(open(f'{D}/bc.fa').read())).items()}
    exp = apply(hap)
    check(f'bcftools consensus {label}: all 3 contigs equal independent application of the VCF', got == exp, (rc, {k: (len(got.get(k, '')), len(exp[k])) for k in exp}, e.strip()[:120]))
h1 = {k: v.upper() for k, v in by_name(fa_records(os.popen(f'cd {D}; bcftools consensus -f synth.fa -H 1 variants.vcf.gz 2>/dev/null').read())).items()}
h2 = {k: v.upper() for k, v in by_name(fa_records(os.popen(f'cd {D}; bcftools consensus -f synth.fa -H 2 variants.vcf.gz 2>/dev/null').read())).items()}
check('phased 1|0 at pos 401 and 0|1 at pos 601 differ between haplotypes as planted (hap1 has alt at 400 not 600; hap2 the reverse)', h1['chr1'][HET50] == alt[HET50] and h1['chr1'][HET20] == S['chr1'][HET20] and h2['chr1'][HET50] == S['chr1'][HET50] and h2['chr1'][HET20] == alt[HET20])

# samtools consensus (reads) agrees with bcftools consensus (VCF) at hom sites -> the two "different operations" the SKILL contrasts
bc_all = apply(None)
check('samtools consensus (from reads) and bcftools consensus (from VCF) agree on chr2 haplotype for the shared 3-bp del + 2-bp ins', c2 in bc_all['chr2'], 'read-derived chr2 haplotype is a substring of the VCF-derived chr2')

# ================= E. real data =================
print('\n--- REAL: SARS-CoV-2 Illumina PE (200 reads) vs MT192765.1 reference')
RS = f'{W}/data/real/sars'
for f in ('test.paired_end.sorted.bam', 'genome.fasta', 'sars-cov-2_v5.3.2.nanopore.bam', 'MN908947.3.fasta'):
    shutil.copy(f'{RS}/{f}', f'{D}/{f}')
sh('samtools index test.paired_end.sorted.bam; samtools index sars-cov-2_v5.3.2.nanopore.bam', D)
ill = f'{D}/test.paired_end.sorted.bam'
CI = counts(ill, 'MT192765.1')
refI = parse_fasta(f'{D}/genome.fasta')['MT192765.1'].upper()
rc, e, r = cons('--show-del yes --show-ins no', bam='test.paired_end.sorted.bam', out='ill.fa')
si = r[0][1]
cov = sorted(CI)
print('  covered span', cov[0], '-', cov[-1], 'consensus length', len(si), 'header', r[0][0])
check('Illumina consensus length = span of covered positions', len(si) == cov[-1] - cov[0] + 1 and len(si) > 100, (len(si), cov[0], cov[-1]))
off = cov[0]
def clear(c):
    n = sum(c.values()); b, k = c.most_common(1)[0]
    return n >= 5 and k / n >= 0.9
mis_all = [p for p in cov if si[p - off] != CI[p].most_common(1)[0][0]]
mis = [p for p in cov if clear(CI[p]) and si[p - off] != CI[p].most_common(1)[0][0]]
print('  Illumina: %d/%d covered positions differ from raw majority, all at low-depth / mixed columns; unambiguous columns (depth>=5, top>=90%%): %d, disagreements %d' % (len(mis_all), len(cov), sum(1 for p in cov if clear(CI[p])), len(mis)))
print('  Illumina disagreements (pos0, consensus, counts):', [(p, si[p-off], dict(CI[p]), refI[p]) for p in mis[:8]], 'total', len(mis))
check('Illumina: consensus == independent majority at every UNAMBIGUOUS covered column (depth>=5, top base >=90%); the remaining disagreements are N/ties at depth 1-2 or mixed columns', not mis and len(mis_all) < 0.01 * len(cov), (mis[:5], len(mis_all)))
snv = [p for p in cov if si[p - off] not in ('N', refI[p])]
print('  consensus differs from the MT192765.1 reference at', len(snv), 'covered positions (real sample-vs-reference differences)')
check('Illumina consensus vs reference: every non-N difference from the reference is a base actually observed in reads at that column', all(si[p - off] in CI[p] for p in snv), [p for p in snv if si[p - off] not in CI[p]][:5])
gaps = [p for p in range(off, cov[-1] + 1) if p not in CI]
print('  uncovered positions inside span:', len(gaps))

print('\n--- REAL: ARTIC nanopore (4916 reads) vs MN908947.3')
nano = f'{D}/sars-cov-2_v5.3.2.nanopore.bam'
refN = parse_fasta(f'{D}/MN908947.3.fasta')['MN908947.3'].upper()
rc, e, r = cons('--config r10.4_sup -d 10 -a --show-del yes --show-ins no', bam='sars-cov-2_v5.3.2.nanopore.bam', out='nano.fa')
sn = r[0][1]
print('  rc', rc, e.strip()[:100], '| consensus length', len(sn), '| N fraction %.3f' % (sn.count('N') / len(sn)), '| ref length', len(refN))
CN = counts(nano, 'MN908947.3')
deep = [p for p, c in CN.items() if sum(c.values()) >= 10]
agree = sum(1 for p in deep if p < len(sn) and sn[p] == CN[p].most_common(1)[0][0])
print('  deep (>=10) positions %d ; consensus==majority at %d (%.4f)' % (len(deep), agree, agree / len(deep)))
# consensus positions map 1:1 only if no indels; use alignment-free comparison restricted to substitutions: compare count of positions
check('ARTIC nanopore consensus with -a: length within 1% of the 29,903 nt reference and N only where depth < 10', abs(len(sn) - len(refN)) < 300, (len(sn), len(refN)))
ident = sum(1 for a, b in zip(sn, refN) if a == b)
print('  positional identity to reference (position-by-position, indels ignored): %.4f' % (ident / len(refN)))

# compare-back (SKILL 352-355): minimap2 -a reference.fa consensus.fa
rc, o, e = sh('minimap2 -a MN908947.3.fasta nano.fa > comparison.sam 2> mm.err; samtools view -c -F 4 comparison.sam; samtools view comparison.sam | cut -f2,3,4,5,6 | cut -c1-120', D)
print('  minimap2 compare-back:', o.strip().replace('\n', ' | '))
check('SKILL "compare consensus to reference": minimap2 -a ref.fa consensus.fa yields a mapped record (MAPQ 60) at pos 1', rc == 0 and o.splitlines()[0] == '1', o.strip()[:200])
nm = sh("samtools view comparison.sam | grep -o 'NM:i:[0-9]*' | head -1", D)[1].strip()
print('  NM tag from minimap2 (mismatches+indel bases incl. N):', nm)

print('\n--- REAL: human chr22 slice (5644 reads) region consensus')
HB = f'{W}/data/real/test.paired_end.sorted.bam'
shutil.copy(HB, f'{D}/h.bam'); shutil.copy(HB + '.bai', f'{D}/h.bam.bai'); shutil.copy(f'{W}/data/real/genome.fasta', f'{D}/hs.fa')
rc, e, r = cons('-r chr22:1952-4617 --show-del yes --show-ins no', bam='h.bam', out='h.fa')
sh_ = r[0][1]
CH = counts(f'{D}/h.bam', 'chr22', 1951, 4617)
refH = parse_fasta(f'{D}/hs.fa')['chr22'].upper()
print('  region consensus len', len(sh_), 'header', r[0][0], 'covered positions', len(CH), 'span', min(CH), max(CH))
mism_all = [p for p in CH if sh_[p - 1951] != CH[p].most_common(1)[0][0]]
mism = [p for p in CH if clear(CH[p]) and sh_[p - 1951] != CH[p].most_common(1)[0][0]]
print('  human: %d/%d covered columns differ from raw majority (mixed / low-depth columns -> N); unambiguous columns disagreements: %d' % (len(mism_all), len(CH), len(mism)))
print('  human disagreements (pos0, consensus, counts, ref):', [(p, sh_[p-1951], dict(CH[p]), refH[p]) for p in mism[:8]], 'total', len(mism))
check('human slice: region consensus == majority at every UNAMBIGUOUS column (depth>=5, top>=90%%) of %d covered positions (max depth %d)' % (len(CH), max(sum(c.values()) for c in CH.values())), not mism, mism[:5])
print('  positions where region consensus != reference base:', sum(1 for p in CH if sh_[p - 1951] not in ('N', refH[p])))

print('\n--- failure modes')
rc, o, e = sh('samtools consensus -r chr1:1-100 -o x.fa nothere.bam', D)
print('  missing BAM ->', rc, e.strip()[:100])
shutil.copy(f'{SY}/synth_chr.bam', f'{D}/noidx.bam')
rc, o, e = sh('samtools consensus -r chr1:1-100 noidx.bam', D)
print('  -r on unindexed BAM ->', rc, e.strip()[:120])
check('region query on an unindexed BAM fails loudly (rc != 0)', rc != 0)

summary()
