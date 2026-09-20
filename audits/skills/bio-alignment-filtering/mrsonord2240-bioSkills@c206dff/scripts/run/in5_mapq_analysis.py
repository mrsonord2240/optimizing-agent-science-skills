#!/usr/bin/env python3
"""Input 5b: evaluate the SKILL.md 'Aligner-Aware MAPQ Thresholds' table on (i) synthetic known-multiplicity
reads for 5 aligners and (ii) the REAL STAR RNA-seq BAM (MAPQ vs NH tag). Retention counted with the real
`samtools view -c -F 2308 -q N` (not pysam), classes from read names."""
import os, subprocess, sys, collections
import pysam

D = sys.argv[1]
AFD = os.environ['AFDATA']
def sh(c): return subprocess.run(c, shell=True, capture_output=True, text=True).stdout

# ---------- real STAR BAM ----------
print('== REAL STAR RNA-seq BAM: MAPQ vs NH (primary records)')
t = collections.Counter()
for r in pysam.AlignmentFile(f'{AFD}/human/test.rna.paired_end.sorted.bam'):
    if r.is_secondary or r.is_unmapped: continue
    nh = r.get_tag('NH') if r.has_tag('NH') else None
    t[(r.mapping_quality, nh)] += 1
for k in sorted(t): print('  MAPQ', k[0], 'NH', k[1], ':', t[k])
tot = sum(t.values())
multi = sum(v for (q, nh), v in t.items() if nh and nh > 1)
for q in (1, 3, 255):
    kept = sum(v for (mq, nh), v in t.items() if mq >= q)
    kept_multi = sum(v for (mq, nh), v in t.items() if mq >= q and nh and nh > 1)
    print(f'  -q {q}: keeps {kept}/{tot} primary; of which NH>1 (multi-mapped) = {kept_multi} (multi total {multi})')

# ---------- synthetic ----------
classes = ['u', 'A2', 'D8', 'B3', 'C5']
cls_desc = {'u': 'unique', 'A2': 'x2 exact', 'D8': 'x8 exact', 'B3': 'x3 1% diverged', 'C5': 'x5 2% diverged'}
def cls(name): return name.split('_')[0]
n_by = collections.Counter()
for l in open(f'{D}/reads.fq'):
    pass
names = [l[1:].strip() for i, l in enumerate(open(f'{D}/reads.fq')) if i % 4 == 0]
for n in names: n_by[cls(n)] += 1
print('\n== SYNTHETIC reads per class', dict(n_by))

def retained(bam, q):
    """dict class -> primary reads with MAPQ>=q (samtools filter, then class from name)"""
    c = collections.Counter()
    out = sh(f'samtools view -F 2308 -q {q} {bam} | cut -f1')
    for nm in out.split():
        c[cls(nm)] += 1
    return c
def mapq_hist(bam, kls):
    h = collections.Counter()
    for l in sh(f'samtools view -F 2308 {bam}').splitlines():
        f = l.split('\t')
        if cls(f[0]) == kls: h[int(f[4])] += 1
    return dict(sorted(h.items()))

rules = {   # aligner: (drop-ambiguous q, high-confidence q) exactly as in the SKILL.md table
    'bwa': (1, 30), 'bowtie2': (1, 23), 'star': (255, 255), 'hisat2': (1, 60), 'minimap2': (1, 60)}
res = {}
for al, (qa, qh) in rules.items():
    bam = f'{D}/{al}.bam'
    print(f'\n-- {al}: MAPQ histogram of primary alignments per class')
    for k in classes: print('   ', f'{k:3s} {cls_desc[k]:15s}', mapq_hist(bam, k))
    ra = retained(bam, qa); rh = retained(bam, qh); r1 = retained(bam, 1)
    print(f'   retained after "drop ambiguous" -q {qa}:', {k: f'{ra[k]}/{n_by[k]}' for k in classes})
    print(f'   retained after "high confidence" -q {qh}:', {k: f'{rh[k]}/{n_by[k]}' for k in classes})
    if qa != 1: print(f'   (universal "-q 1" would retain):', {k: f'{r1[k]}/{n_by[k]}' for k in classes})
    res[al] = (ra, rh, r1)

print('\n== Verdict per SKILL.md claim: fraction of TRULY AMBIGUOUS EXACT-repeat reads (A2+D8) that survive')
ex = n_by['A2'] + n_by['D8']
for al, (qa, qh) in rules.items():
    ra, rh, r1 = res[al]
    print(f'  {al:9s} "-q {qa}" (drop ambiguous): {ra["A2"]+ra["D8"]}/{ex} exact-repeat reads kept ;',
          f'"-q {qh}" (high conf): {rh["A2"]+rh["D8"]}/{ex} kept, unique kept {rh["u"]}/{n_by["u"]} ;',
          f'universal -q 1: {r1["A2"]+r1["D8"]}/{ex} kept')
