"""Independent check of Picard's genic/intergenic split on real chrX from the BED12 (transcript span union) and pysam aligned blocks.
Also round-trips the SKILL.md awk refFlat back to BED12 blocks. Usage: python 72_in7_real_picard.py bam bed12 refFlat metrics"""
import sys, bisect, pysam
bam, bed, rf, met = sys.argv[1:5]
# 1. refFlat <-> BED12 round trip
n = bad = 0
b = {}
for l in open(bed):
    f = l.rstrip('\n').split('\t')
    sz = list(map(int, f[10].strip(',').split(','))); st = list(map(int, f[11].strip(',').split(',')))
    b[f[3]] = (f[0], f[5], int(f[1]), int(f[2]), [(int(f[1]) + s, int(f[1]) + s + z) for s, z in zip(st, sz)], int(f[6]), int(f[7]))
for l in open(rf):
    f = l.rstrip('\n').split('\t'); n += 1
    ex = list(zip(map(int, f[9].strip(',').split(',')), map(int, f[10].strip(',').split(','))))
    t = b[f[1]]
    if not (f[2] == t[0] and f[3] == t[1] and int(f[4]) == t[2] and int(f[5]) == t[3] and ex == t[4] and int(f[6]) == t[5] and int(f[7]) == t[6] and int(f[8]) == len(ex)): bad += 1
print('refFlat lines', n, 'bed12 lines', len(b), 'lines that differ from the BED12 blocks:', bad)
# 2. union of transcript spans
spans = sorted((t[2], t[3]) for t in b.values()); merged = []
for s, e in spans:
    if merged and s <= merged[-1][1]: merged[-1][1] = max(merged[-1][1], e)
    else: merged.append([s, e])
starts = [m[0] for m in merged]
def genic(s, e):
    tot = 0; i = max(bisect.bisect(starts, s) - 1, 0)
    while i < len(merged) and merged[i][0] < e:
        tot += max(0, min(e, merged[i][1]) - max(s, merged[i][0])); i += 1
    return tot
al = gen = 0
for r in pysam.AlignmentFile(bam).fetch(until_eof=True):
    if r.is_unmapped or r.is_secondary or r.is_supplementary or r.is_duplicate or r.is_qcfail: continue
    pos = r.reference_start
    for op, ln in r.cigartuples:
        if op in (0, 7, 8): al += ln; gen += genic(pos, pos + ln); pos += ln
        elif op in (2, 3): pos += ln
print('independent: aligned bases %d, in a transcript span %.4f, intergenic %.4f' % (al, gen / al, 1 - gen / al))
h = None
for l in open(met):
    if l.startswith('PF_BASES'): h = l.rstrip('\n').split('\t'); continue
    if h and l.strip():
        v = dict(zip(h, l.rstrip('\n').split('\t')))
        print('Picard   : PF_ALIGNED_BASES %s, PCT_CODING %s UTR %s INTRONIC %s INTERGENIC %s -> genic %.4f, sum %.4f, 5p/3p bias %s, correct strand %s' % (v['PF_ALIGNED_BASES'], v['PCT_CODING_BASES'], v['PCT_UTR_BASES'], v['PCT_INTRONIC_BASES'], v['PCT_INTERGENIC_BASES'], 1 - float(v['PCT_INTERGENIC_BASES']), sum(float(v[k]) for k in ('PCT_CODING_BASES', 'PCT_UTR_BASES', 'PCT_INTRONIC_BASES', 'PCT_INTERGENIC_BASES')), v['MEDIAN_5PRIME_TO_3PRIME_BIAS'], v['PCT_CORRECT_STRAND_READS']))
        break
