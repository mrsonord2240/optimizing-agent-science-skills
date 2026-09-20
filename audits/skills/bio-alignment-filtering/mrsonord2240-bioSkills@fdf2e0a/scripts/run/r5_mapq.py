#!/usr/bin/env python3
"""Input 5 (regression, Stress): the FIXED 'Aligner-Aware MAPQ Thresholds' table + the new NH paragraph, on
(i) SYNTHETIC reads of known multiplicity aligned with 5 aligners (BWA 0.7.19, Bowtie2 2.5.5, HISAT2 2.2.3,
minimap2 2.31, STAR 2.7.11b) and (ii) the REAL STAR RNA-seq BAM (MAPQ vs NH). Retention is counted with the real
`samtools view -c -F 2308 -q N` / `-e '[NH]==1'`; classes come from read names (truth), not from the aligner.
Table rows are read out of the SKILL.md itself and the numbers quoted in the prose are compared with what was measured."""
import collections, os, re, subprocess, sys
import pysam
from lib import check, sh, finish

D, SK = sys.argv[1], sys.argv[2]
AFD = os.environ['AFDATA']
txt = open(f'{SK}/SKILL.md', encoding='utf-8').read()

# ---- parse the table from the text ----
sec = txt[txt.index('### Aligner-Aware MAPQ Thresholds'):txt.index('## Filter by Region')]
rows = {}
for line in sec.splitlines():
    m = re.match(r'\|\s*\**([A-Za-z0-9/\-\. ]+?)(?: \(.*?\))?\**\s*\|\s*`-q (\d+)`.*?\|\s*`-q (\d+)`', line)
    if m: rows[m.group(1).strip()] = (int(m.group(2)), int(m.group(3)))
print('parsed table rows:', rows)
want = {'BWA-MEM / BWA-MEM2': (1, 30), 'Bowtie2': (2, 23), 'STAR': (255, 255), 'HISAT2': (2, 60), 'minimap2': (1, 60), 'pbmm2': (1, 60)}
check('table parsed: 6 rows with the thresholds the text shows', rows == want, str(rows))
rules = {'bwa': rows['BWA-MEM / BWA-MEM2'], 'bowtie2': rows['Bowtie2'], 'star': rows['STAR'], 'hisat2': rows['HISAT2'], 'minimap2': rows['minimap2']}

def cls(n): return n.split('_')[0]
names = [l[1:].strip() for i, l in enumerate(open(f'{D}/reads.fq')) if i % 4 == 0]
n_by = collections.Counter(cls(n) for n in names)
print('reads per class', dict(n_by), '(u unique; A2/D8 exact repeats x2/x8; B3/C5 diverged repeats x3/x5)')
def retained(bam, q, expr=None):
    e = f"-e '{expr}'" if expr else ''
    out = sh(f'samtools view -F 2308 -q {q} {e} {bam} | cut -f1')[1]
    return collections.Counter(cls(n) for n in out.split())
def hist(bam, k):
    h = collections.Counter()
    for l in sh(f'samtools view -F 2308 {bam}')[1].splitlines():
        f = l.split('\t')
        if cls(f[0]) == k: h[int(f[4])] += 1
    return dict(sorted(h.items()))
ex_total = n_by['A2'] + n_by['D8']
res = {}
for al, (qa, qh) in rules.items():
    bam = f'{D}/{al}.bam'
    print(f'\n-- {al}: MAPQ histogram of primary alignments per class')
    for k in ('u', 'A2', 'D8', 'B3', 'C5'): print('   ', k, hist(bam, k))
    ra = retained(bam, qa); rh = retained(bam, qh); r1 = retained(bam, 1); r0 = retained(bam, 0)
    exa = ra['A2'] + ra['D8']
    res[al] = dict(exa=exa, exh=rh['A2'] + rh['D8'], uh=rh['u'], u_a=ra['u'], q1=r1['A2'] + r1['D8'], div=(ra['B3'] + ra['C5']), total_u=n_by['u'])
    print(f'   drop-ambiguous -q {qa}: exact-repeat kept {exa}/{ex_total}; unique kept {ra["u"]}/{n_by["u"]}; diverged-repeat kept {ra["B3"]+ra["C5"]}/{n_by["B3"]+n_by["C5"]}')
    print(f'   high-confidence -q {qh}: exact-repeat kept {rh["A2"]+rh["D8"]}/{ex_total}; unique kept {rh["u"]}/{n_by["u"]}')
    print(f'   old/naive -q 1: exact-repeat kept {r1["A2"]+r1["D8"]}/{ex_total}')
    check(f'{al}: table "drop ambiguous" -q {qa} removes 400/400 exact-repeat reads', exa == 0, f'{exa} of {ex_total} survive')
    check(f'{al}: table "high confidence" -q {qh} removes 400/400 exact-repeat reads', res[al]['exh'] == 0, f'{res[al]["exh"]} survive')
    check(f'{al}: "drop ambiguous" keeps >= 97% of the {n_by["u"]} unique reads', ra['u'] >= 0.97 * n_by['u'], f'{ra["u"]}/{n_by["u"]}')
    check(f'{al}: "high confidence" keeps >= 90% of unique reads', rh['u'] >= 0.90 * n_by['u'], f'{rh["u"]}/{n_by["u"]}')

# ---- numbers quoted in the prose ----
check('prose: "-q 1 kept 399/400 (Bowtie2)"', res['bowtie2']['q1'] == 399, str(res['bowtie2']['q1']))
check('prose: "-q 1 kept 374/400 (HISAT2)"', res['hisat2']['q1'] == 374, str(res['hisat2']['q1']))
check('prose: "-q 1 kept 80/400 (STAR)"', res['star']['q1'] == 80, str(res['star']['q1']))
check('prose: -q 1 removes all exact repeats for BWA and minimap2', res['bwa']['q1'] == 0 and res['minimap2']['q1'] == 0, f'bwa {res["bwa"]["q1"]} minimap2 {res["minimap2"]["q1"]}')

# ---- STAR MAPQ set and the -q 4..255 equivalence ----
star = f'{D}/star.bam'
allq = collections.Counter(int(l.split('\t')[4]) for l in sh(f'samtools view -F 2308 {star}')[1].splitlines())
print('STAR MAPQ values over all primary mapped records:', dict(sorted(allq.items())))
check('STAR emits only MAPQ {0,1,3,255} (prose)', set(allq) <= {0, 1, 3, 255}, str(sorted(allq)))
cnts = {q: int(sh(f'samtools view -c -F 2308 -q {q} {star}')[1]) for q in (4, 60, 100, 255)}
check('STAR: -q 4 == -q 60 == -q 255 (prose: all equivalent)', len(set(cnts.values())) == 1, str(cnts))
# NH tag semantic
nh = collections.Counter()
for r in pysam.AlignmentFile(star):
    if r.is_secondary or r.is_unmapped: continue
    nh[(r.mapping_quality, r.get_tag('NH'))] += 1
print('STAR (MAPQ, NH) -> n:', dict(sorted(nh.items())))
check('STAR MAPQ 255 <=> NH==1; 3 <=> NH==2; 1 <=> NH 3-4; 0 <=> NH>4 (prose)', all((q == 255) == (n == 1) and (q != 3 or n == 2) and (q != 1 or n in (3, 4)) and (q != 0 or n > 4) for (q, n) in nh), '')
a = int(sh(f"samtools view -c -F 2308 -e '[NH]==1' {star}")[1]); b = cnts[255]
check("STAR: -e '[NH]==1' count == -q 255 count", a == b, f'{a} vs {b}')
ra = retained(star, 0, '[NH]==1'); print('   STAR -e [NH]==1 exact-repeat kept', ra['A2'] + ra['D8'])
# HISAT2
h = f'{D}/hisat2.bam'
a = retained(h, 0, '[NH]==1')
print(f'   HISAT2 -e [NH]==1: exact kept {a["A2"]+a["D8"]}/{ex_total}; unique kept {a["u"]}/{n_by["u"]}')
check("HISAT2: -e '[NH]==1' removes 400/400 exact repeats (prose)", a['A2'] + a['D8'] == 0)
hq = collections.Counter()
for r in pysam.AlignmentFile(h):
    if r.is_secondary or r.is_unmapped: continue
    hq[(r.mapping_quality, r.get_tag('NH'))] += 1
print('HISAT2 (MAPQ, NH) -> n:', dict(sorted(hq.items())))
# BWA / Bowtie2 / minimap2: no NH -> silently empty
for al in ('bwa', 'bowtie2', 'minimap2'):
    n = int(sh(f"samtools view -c -e '[NH]==1' {D}/{al}.bam")[1])
    rc, so, se = sh(f"samtools view -c -e '[NH]==1' {D}/{al}.bam")
    check(f"{al}: -e '[NH]==1' returns 0 with rc 0 and no warning (prose)", n == 0 and rc == 0 and se.strip() == '', f'n={n} rc={rc} err={se.strip()!r}')
# Bowtie2 MAPQ max
bq = collections.Counter(int(l.split('\t')[4]) for l in sh(f'samtools view -F 2308 {D}/bowtie2.bam')[1].splitlines())
print('Bowtie2 MAPQ values:', dict(sorted(bq.items())))
check('Bowtie2 end-to-end MAPQ max is 42 (prose)', max(bq) == 42, f'max {max(bq)}')
check('Bowtie2 multi-mapper MAPQ is 0 or 1 only', all(int(l.split("\t")[4]) <= 1 for l in sh(f'samtools view -F 2308 {D}/bowtie2.bam')[1].splitlines() if cls(l.split("\t")[0]) in ('A2', 'D8')))
hq2 = collections.Counter(int(l.split('\t')[4]) for l in sh(f'samtools view -F 2308 {D}/hisat2.bam')[1].splitlines() if cls(l.split('\t')[0]) in ('A2', 'D8'))
print('HISAT2 exact-repeat MAPQ values:', dict(hq2))
check('HISAT2 multi-mapper MAPQ is 0 or 1 only', set(hq2) <= {0, 1}, str(dict(hq2)))
# ---- REAL STAR BAM ----
rna = f'{AFD}/human/test.rna.paired_end.sorted.bam'
t = collections.Counter()
for r in pysam.AlignmentFile(rna):
    if r.is_secondary or r.is_unmapped: continue
    t[(r.mapping_quality, r.get_tag('NH') if r.has_tag('NH') else None)] += 1
print('REAL STAR BAM (MAPQ, NH) -> n:', dict(sorted(t.items())))
tot = sum(t.values())
check('real STAR BAM: MAPQ 255 <=> NH==1 for every primary record (prose says 5768)', all((q == 255) == (n == 1) for (q, n) in t) and sum(v for (q, n), v in t.items() if q == 255 and n == 1) + sum(v for (q, n), v in t.items() if q != 255 and n != 1) == tot, f'total primary {tot}')
print('   text quotes "5768 records": measured', tot, '(all primary+secondary?)', int(sh(f'samtools view -c -F 4 {rna}')[1]))
a = int(sh(f"samtools view -c -e '[NH]==1' {rna}")[1]); b = int(sh(f'samtools view -c -q 255 {rna}')[1])
check("real STAR BAM: -e '[NH]==1' == -q 255 (all records)", a == b, f'{a} vs {b}')
finish()
