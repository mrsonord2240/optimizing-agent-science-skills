#!/usr/bin/env python3
"""NEW input 9 (Stress): the 'pbmm2 (PacBio) -q 1 / -q 60' and 'minimap2 (DNA, long-read)' rows, which the fixer left unrun, plus the
long-read assay rows (`-F 3328 -q 5`, SV `-F 1024`) on the REAL ARTIC nanopore BAM (4916 records).
SYNTHETIC long reads (n9_make_longreads.py; class truth in the read name): pbmm2 26.2.99 --preset CCS / SUBREAD, minimap2 map-hifi / map-ont."""
import collections, os, re, sys
import pysam
from lib import check, sh, finish

D, SK = sys.argv[1], sys.argv[2]
AFD = os.environ['AFDATA']
txt = open(f'{SK}/SKILL.md', encoding='utf-8').read()
check('SKILL.md pbmm2 row: `-q 1` drop ambiguous / `-q 60` high confidence', re.search(r'\| pbmm2 \(PacBio\) \| `-q 1` \| `-q 60` \|', txt) is not None)
check('SKILL.md minimap2 row: (DNA, long-read) `-q 1` / `-q 60`', re.search(r'\| minimap2 \(DNA, long-read\) \| `-q 1` \| `-q 60` \|', txt) is not None)
check('SKILL.md says the pbmm2 row was not run (honest caveat)', 'The pbmm2 row was not run' in txt)
def cls(n): return n.split('_')[0]
names = [l[1:].strip() for i, l in enumerate(open(f'{D}/hifi.fq')) if i % 4 == 0]
nby = collections.Counter(cls(n) for n in names)
print('reads per class:', dict(nby), '(u unique; A2 exact x2; B3 1% x3; C2 8% x2)')
def prim(bam): return [l.split('\t') for l in sh(f'samtools view -F 2308 {bam}')[1].splitlines()]
res = {}
for tag in ('pbmm2_hifi', 'pbmm2_ont', 'mm2_hifi', 'mm2_ont'):
    rows = prim(f'{D}/{tag}.bam')
    h = collections.defaultdict(collections.Counter)
    for x in rows: h[cls(x[0])][int(x[4])] += 1
    print(f'\n-- {tag}: {len(rows)} primary records; MAPQ summary per class (min/median/max, share of MAPQ 60, share of MAPQ 0)')
    for k in ('u', 'A2', 'B3', 'C2'):
        v = sorted(q for q, c in h[k].items() for _ in range(c))
        print(f'   {k:3s} n={len(v):3d} min {v[0]:2d} med {v[len(v)//2]:2d} max {v[-1]:2d}  MAPQ60 {sum(1 for q in v if q == 60)/len(v):.0%}  MAPQ0 {sum(1 for q in v if q == 0)/len(v):.0%}  MAPQ>=1 {sum(1 for q in v if q >= 1)}/{len(v)}  MAPQ>=5 {sum(1 for q in v if q >= 5)}/{len(v)}')
    keep1 = collections.Counter(cls(x[0]) for x in rows if int(x[4]) >= 1); keep60 = collections.Counter(cls(x[0]) for x in rows if int(x[4]) >= 60)
    # the same, through the real samtools filter (second method)
    s1 = collections.Counter(cls(n) for n in sh(f'samtools view -F 2308 -q 1 {D}/{tag}.bam | cut -f1')[1].split())
    s60 = collections.Counter(cls(n) for n in sh(f'samtools view -F 2308 -q 60 {D}/{tag}.bam | cut -f1')[1].split())
    check(f'{tag}: samtools -q 1 / -q 60 retention == direct MAPQ count', s1 == keep1 and s60 == keep60)
    res[tag] = (s1, s60)
    print(f'   -q 1 keeps: unique {s1["u"]}/{nby["u"]}, exact repeat {s1["A2"]}/{nby["A2"]}, 1%-diverged {s1["B3"]}/{nby["B3"]}, 8%-diverged {s1["C2"]}/{nby["C2"]}')
    print(f'   -q 60 keeps: unique {s60["u"]}/{nby["u"]}, exact repeat {s60["A2"]}/{nby["A2"]}, 1%-diverged {s60["B3"]}/{nby["B3"]}, 8%-diverged {s60["C2"]}/{nby["C2"]}')
for tag in ('pbmm2_hifi', 'pbmm2_ont'):
    s1, s60 = res[tag]
    check(f'{tag}: table `-q 1` ("drop ambiguous") removes 80/80 exact-repeat reads', s1['A2'] == 0, f'{s1["A2"]} survive')
    check(f'{tag}: table `-q 60` ("high confidence") removes 80/80 exact-repeat reads', s60['A2'] == 0, f'{s60["A2"]} survive')
    check(f'{tag}: `-q 60` keeps >= 90% of unique reads', s60['u'] >= 0.9 * nby['u'], f'{s60["u"]}/{nby["u"]}')
    check(f'{tag}: `-q 1` keeps >= 97% of unique reads', s1['u'] >= 0.97 * nby['u'], f'{s1["u"]}/{nby["u"]}')
for tag in ('mm2_hifi', 'mm2_ont'):
    s1, s60 = res[tag]
    check(f'{tag}: minimap2 row `-q 1` removes 80/80 exact repeats', s1['A2'] == 0, f'{s1["A2"]}')
    check(f'{tag}: minimap2 row `-q 60` removes 80/80 exact repeats and keeps >= 90% unique', s60['A2'] == 0 and s60['u'] >= 0.9 * nby['u'], f'exact {s60["A2"]}, unique {s60["u"]}/{nby["u"]}')
# pbmm2 vs minimap2 agreement (same core aligner)
pa = {x[0]: int(x[4]) for x in prim(f'{D}/pbmm2_hifi.bam')}; ma = {x[0]: int(x[4]) for x in prim(f'{D}/mm2_hifi.bam')}
same = sum(1 for k in pa if pa[k] == ma[k]); print(f'\npbmm2 CCS vs minimap2 map-hifi MAPQ identical for {same}/{len(pa)} reads')
# the 8%-diverged copies: what does "-q 1 drop ambiguous" do to them
print('note: 8%-diverged repeats (C2) are placed with MAPQ that depends on the divergence, not multiplicity; see per-class summaries above')

# ---- REAL nanopore BAM ----
ont = f'{AFD}/sarscov2/sars-cov-2_v5.3.2.nanopore.bam'
print('\n=== REAL ARTIC nanopore BAM')
hd = sh(f'samtools view -H {ont} | grep ^@PG')[1].strip().splitlines()
print('  @PG:', [h[:90] for h in hd][:2])
rows = [l.split('\t') for l in sh(f'samtools view {ont}')[1].splitlines()]
n = len(rows); h = collections.Counter(int(x[4]) for x in rows)
supp = sum(1 for x in rows if int(x[1]) & 2048); sec = sum(1 for x in rows if int(x[1]) & 256); un = sum(1 for x in rows if int(x[1]) & 4)
print(f'  records {n}; MAPQ counts (top): {dict(sorted(h.items())[:4])} ... 60: {h[60]}; supplementary {supp}; secondary {sec}; unmapped {un}')
c = lambda a: int(sh(f'samtools view -c {a} {ont}')[1])
truth = lambda pred: sum(1 for x in rows if pred(int(x[1]), int(x[4])))
check('long-read short-variant recipe `-F 3328 -q 5` == bit arithmetic on the real ONT BAM', c('-F 3328 -q 5') == truth(lambda f, q: not f & 3328 and q >= 5), f'{c("-F 3328 -q 5")} of {n}')
check('SV recipe `-F 1024` keeps every record (no dup flags) and every supplementary one', c('-F 1024') == n and c('-f 2048 -F 1024') == supp, f'{c("-F 1024")}; supp {supp}')
print(f'  `-q 60` keeps {c("-q 60")}/{n}; `-q 1` keeps {c("-q 1")}/{n}; `-F 3328 -q 5` keeps {c("-F 3328 -q 5")}/{n}; -F 3332 removes {c("-f 2048")} supplementary that an SV caller would want')
print(f'  fixture note: the real ONT BAM holds {supp} supplementary records, so the SV-row supplementary claim is exercised on the synthetic flag BAM (r2/r7), not on real long reads')
finish()
