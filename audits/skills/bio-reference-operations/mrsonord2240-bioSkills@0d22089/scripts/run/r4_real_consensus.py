#!/usr/bin/env python
"""INPUTS 4 and 5 (regression of pre-fix inputs 4 and 5) on REAL data: the SKILL's consensus commands and its Python build_consensus / compare_to_ref
(verbatim from SKILL.md) on the human chr22 slice, the 1000G HG00349 chr20 slice, the SARS-CoV-2 Illumina BAM and the ARTIC nanopore BAM.
Second method everywhere: samtools mpileup majority (independent parser) and samtools consensus; external truth where available (Ensembl chr20 sequence)."""
import json, os, re, shutil, sys
from collections import Counter
sys.path.insert(0, '/mnt/openscience/audits/bio-reference-operations/run')
from auditlib import *
import pysam
D = f'{W}/work/r4'; shutil.rmtree(D, ignore_errors=True); os.makedirs(D)
R = f'{W}/data/real'
def blk(n): return open(f'{W}/snippets/{n}.txt').read()
ns = {'pysam': pysam, 'Counter': Counter}
exec(blk('skill_25_python'), ns); exec(blk('skill_26_python'), ns)
bc, cmp_ = ns['build_consensus'], ns['compare_to_ref']

def mpileup_majority(bam, ref, region, start1, end1, minq=13):
    """independent parser of samtools mpileup output (-B: no BAQ, as pysam pileup has none) -> {pos1: (base, depth)} (majority of ACGT, ties -> None)"""
    rc, o, e = sh(f'samtools mpileup -B -Q {minq} -q 0 -d 8000000 -r {region} -f {ref} {bam}', D)
    out = {}
    for ln in o.splitlines():
        f = ln.split('\t'); pos = int(f[1]); rb = f[2].upper(); bases = f[4]
        i = 0; c = Counter()
        while i < len(bases):
            ch = bases[i]
            if ch == '^': i += 2; continue
            if ch == '$': i += 1; continue
            if ch in '+-':
                m = re.match(r'[+-](\d+)', bases[i:]); n = int(m.group(1)); i += len(m.group(0)) + n; continue
            if ch in '.,': c[rb] += 1
            elif ch.upper() in 'ACGT': c[ch.upper()] += 1
            i += 1
        if c:
            top = c.most_common(2)
            out[pos] = (top[0][0] if len(top) == 1 or top[0][1] > top[1][1] else None, sum(c.values()))
    return out

print('##### INPUT 5 (regression): human chr22 slice 1952-4617 (real, PE)')
ref = f'{R}/genome.fasta'; bam = f'{R}/test.paired_end.sorted.bam'
cons = bc(bam, 'chr22', 1951, 4617)
check('build_consensus (verbatim) returns exactly 2666 chars for [1951,4617) (pre-fix version returned 1157: shifted after gaps)', len(cons) == 2666, len(cons))
mp = mpileup_majority(bam, ref, 'chr22:1952-4617', 1952, 4617)
called = [i for i in range(2666) if cons[i] != 'N']
mism = [i for i in range(2666) if (i + 1952) in mp and mp[i + 1952][1] >= 3 and mp[i + 1952][0] and cons[i] != mp[i + 1952][0]]
check('build_consensus equals the mpileup -B -Q13 majority (independent parser) at every column with depth>=3 and no tie (n=%d)' % sum(1 for p in mp.values() if p[1] >= 3 and p[0]), not mism, mism[:10])
uncovered = [i for i in range(2666) if (i + 1952) not in mp]
check('all %d columns with no mpileup coverage are N in place (index i == position 1952+i)' % len(uncovered), all(cons[i] == 'N' for i in uncovered))
diffs = cmp_(bam, ref, 'chr22', 1951, 4617)
print('    compare_to_ref ->', diffs)
sm = sh(f'samtools consensus -m simple --call-fract 0.5 --min-BQ 13 -d 3 -a --show-del yes --show-ins no -r chr22:1952-4617 {bam}', D)[1]
smc = ''.join(l for l in sm.splitlines() if not l.startswith('>'))
refseq = parse_fasta(ref)['chr22'][1951:4617].upper()
sm_diffs = [(1952 + i, refseq[i], smc[i]) for i in range(len(smc)) if smc[i] not in 'N*' and smc[i] != refseq[i]]
print('    samtools consensus -m simple differences:', sm_diffs)
check('compare_to_ref list == samtools consensus -m simple difference list on the real slice', [tuple(x) for x in diffs] == sm_diffs, (diffs, sm_diffs))
sb = sh(f'samtools consensus -d 3 -a --show-del yes --show-ins no -r chr22:1952-4617 {bam}', D)[1]; sbc = ''.join(l for l in sb.splitlines() if not l.startswith('>'))
sb_diffs = [(1952 + i, refseq[i], sbc[i]) for i in range(len(sbc)) if sbc[i] not in 'N*' and sbc[i] != refseq[i]]
print('    samtools consensus (default Bayesian) differences:', sb_diffs, '| SKILL says: 1 by majority/simple, 2 by default Bayesian')
check('SKILL statement (chr22 slice: 1 difference by majority vote and by -m simple --call-fract 0.5 --min-BQ 13, 2 by default Bayesian) reproduces WITH -d 3 (the SKILL sentence omits -d 3)', len(diffs) == 1 and len(sm_diffs) == 1 and len(sb_diffs) == 2, (len(diffs), len(sm_diffs), len(sb_diffs)))
sm1 = ''.join(l for l in sh(f'samtools consensus -m simple --call-fract 0.5 --min-BQ 13 -a --show-del yes --show-ins no -r chr22:1952-4617 {bam}', D)[1].splitlines() if not l.startswith('>'))
n1 = [(1952 + i) for i in range(len(sm1)) if sm1[i] not in 'N*' and sm1[i] != refseq[i]]
sb1 = ''.join(l for l in sh(f'samtools consensus -a --show-del yes --show-ins no -r chr22:1952-4617 {bam}', D)[1].splitlines() if not l.startswith('>'))
n2 = [(1952 + i) for i in range(len(sb1)) if sb1[i] not in 'N*' and sb1[i] != refseq[i]]
print('    WITHOUT -d 3 (default -d 1): simple differences at', n1, '| Bayesian differences at', n2)
check('OBSERVATION: with the options exactly as printed in the SKILL sentence (no -d) the counts are 5 (simple) and 4 (Bayesian), not 1 and 2', len(n1) == 5 and len(n2) == 4, (n1, n2))
both = [i for i in range(2666) if cons[i] in 'ACGT' and sbc[i] in 'ACGT']; dis = [i for i in both if cons[i] != sbc[i]]
print('    columns called ACGT by both build_consensus and default samtools consensus:', len(both), '; disagreements:', len(dis))
# lower-case reference
open(f'{D}/lower.fa', 'w').write('>chr22\n' + '\n'.join(parse_fasta(ref)['chr22'].lower()[j:j + 60] for j in range(0, 40001, 60)) + '\n')
d_low = cmp_(bam, f'{D}/lower.fa', 'chr22', 1951, 4617)
check('compare_to_ref on an all-lower-case copy of the reference gives the same result (case-insensitive)', d_low == diffs, d_low)
# max_depth: depth up to 2532 on this slice; default 8000 fine; the SKILL raised max_depth: compare with a 100-depth cap
capped = bc(bam, 'chr22', 1951, 4617)
check('deep columns (depth up to 2532): the consensus calls %d columns at min_depth 3; max_depth raise means no subsampling (called columns == columns with mpileup depth>=3)' % len(called), len(called) == sum(1 for p in mp.values() if p[1] >= 3), (len(called), sum(1 for p in mp.values() if p[1] >= 3)))

print('##### INPUT 5b: 1000G HG00349 chr20:1,400,001-1,500,000 (real low-coverage WGS) vs Ensembl truth')
g = f'{R}/g1000/chr20_padded_1500000.fa'; gb = f'{R}/g1000/HG00349.chr20_1400000-1500000.bam'
ens = open(f'{R}/g1000/chr20_1400001-1500000.seq.txt').read().strip().upper()
c20 = bc(gb, 'chr20', 1400000, 1500000, min_depth=3)
check('build_consensus on 100 kb: exactly 100000 chars', len(c20) == 100000, len(c20))
mp20 = mpileup_majority(gb, g, 'chr20:1400001-1500000', 1400001, 1500000)
m20 = [i for i in range(100000) if (1400001 + i) in mp20 and mp20[1400001 + i][1] >= 3 and mp20[1400001 + i][0] and c20[i] != mp20[1400001 + i][0]]
check('build_consensus == mpileup -B -Q13 majority at every column with depth>=3 and no tie (independent parser; n=%d)' % sum(1 for p in mp20.values() if p[1] >= 3 and p[0]), not m20, m20[:8])
d20 = cmp_(gb, g, 'chr20', 1400000, 1500000)
# external truth: the reference used is Ensembl's sequence, so compare_to_ref result must equal a direct diff against ens
ext = [(1400001 + i, ens[i], c20[i]) for i in range(100000) if c20[i] != 'N' and c20[i] != ens[i]]
check('compare_to_ref on the padded reference == direct comparison of the consensus with the independent Ensembl sequence (%d differences)' % len(ext), [tuple(x) for x in d20] == ext, (len(d20), len(ext)))
ncalled = sum(1 for c in c20 if c != 'N')
print('    called columns (depth>=3):', ncalled, 'differences vs GRCh38:', len(ext), '=> %.2f per kb' % (1000 * len(ext) / max(ncalled, 1)))
check('sanity: a real HG00349 slice differs from GRCh38 at < 5 per kb of called sequence (SNP density scale)', len(ext) / max(ncalled, 1) < 0.005, len(ext) / ncalled)
sb20 = sh(f'samtools consensus -a --show-del yes --show-ins no -d 3 -r chr20:1400001-1500000 {gb}', D)[1]; s20 = ''.join(l for l in sb20.splitlines() if not l.startswith('>'))
print('    samtools consensus -a on the 100 kb slice: length', len(s20))
both = [i for i in range(min(len(s20), 100000)) if s20[i] in 'ACGT' and c20[i] in 'ACGT']
dd = [i for i in both if s20[i] != c20[i]]
print('    columns called by both:', len(both), 'disagreements (majority vs Bayesian, quality-weighted):', len(dd))
check('samtools consensus (Bayesian) and the majority vote agree at >= 99.5% of jointly called columns on real low-coverage data', len(dd) / max(len(both), 1) < 0.005, (len(dd), len(both)))

print('##### INPUT 4 (regression): SKILL viral consensus command, verbatim, on the real SARS-CoV-2 Illumina BAM and the ARTIC nanopore BAM')
cmd = [l for l in blk('skill_19_bash').splitlines() if l.startswith('samtools consensus')][0]
print('    SKILL command:', cmd)
sv = f'{R}/sars/test.paired_end.sorted.bam'
rc, o, e = sh(cmd.replace('input.bam', sv).replace('-o consensus.fa', '-o cons_ill.fa'), D)
recs = fa_records(open(f'{D}/cons_ill.fa').read())
seq = recs[0][1]
dep = {}
for l in sh(f'samtools depth -a -q 0 -Q 0 {sv}', D)[1].splitlines():
    a = l.split('\t'); dep[int(a[1])] = int(a[2])
L = 29829
rc2, o2, e2 = sh(cmd.replace('input.bam', sv).replace('-o consensus.fa', '--show-del yes --show-ins no'), D)
seq_al = ''.join(l for l in o2.splitlines() if not l.startswith('>'))
print('    viral command as printed: len', len(seq), '| same command + --show-del yes --show-ins no: len', len(seq_al), '(header LN', L, ')')
check('viral command: 1 record, no * in the FASTA; with --show-del yes --show-ins no it is exactly the header LN 29829 (-a pads to the ends; deletions are not shown by default)', len(recs) == 1 and '*' not in seq and len(seq_al) == L, (len(recs), len(seq), len(seq_al)))
seq = seq_al
lowN = [p for p in range(1, L + 1) if dep.get(p, 0) < 10]
nN = [p for p in range(1, L + 1) if seq[p - 1] == 'N']
star = [p for p in range(1, L + 1) if seq[p - 1] == '*']
check('every position with samtools depth < 10 is N (or * at a deleted column) in the aligned-length consensus (-d 10); no N at depth >= 10', all(seq[p - 1] in 'N*' for p in lowN) and not [p for p in nN if dep.get(p, 0) >= 10], (len(lowN), len(nN), len(star)))
sref = parse_fasta(f'{R}/sars/genome.fasta')['MT192765.1'].upper()
diff = [p for p in range(1, L + 1) if seq[p - 1] in 'ACGT' and seq[p - 1] != sref[p - 1]]
print('    Illumina viral consensus (nf-core test BAM has only 200 reads, so almost every column is below -d 10): called %d, N %d, * %d, differences from MT192765.1: %d' % (sum(1 for c in seq if c in 'ACGT'), len(nN), len(star), len(diff)))
check('called bases match the reference it was aligned to at >= 99% (nf-core test reads simulated from the reference)', len(diff) <= 0.01 * max(sum(1 for c in seq if c in 'ACGT'), 1), len(diff))
# ARTIC nanopore: default and the SKILL --config r10.4_sup path (help lists it)
nb = f'{R}/sars/sars-cov-2_v5.3.2.nanopore.bam'
rc, o, e = sh(f'samtools consensus --config r10.4_sup -d 10 --ambig -a {nb}', D)
recs = fa_records(o); nseq = recs[0][1] if recs else ''
mref = parse_fasta(f'{R}/sars/MN908947.3.fasta')['MN908947.3'].upper()
print('    nanopore ARTIC (r10.4_sup profile, whatever the chemistry): rc', rc, 'len', len(nseq), 'N', nseq.count('N'), e.strip()[:150])
called = [i for i in range(len(nseq)) if nseq[i] in 'ACGT']
ident = sum(1 for i in called if nseq[i] == mref[i]) / max(len(called), 1)
check('ARTIC nanopore consensus: one record of 29903 bp, >= 98% identical to MN908947.3 over called bases (Wuhan-Hu-1 vs a Wuhan-lineage amplicon set)', len(nseq) == 29903 and ident > 0.98, (len(nseq), round(ident, 4)))
summary()
