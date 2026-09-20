#!/usr/bin/env python3
"""Per-read intron chains of two alignments of the same reads (e.g. --junc-bonus default vs 16 on REAL reads): how many reads change chain, and of the changed reads
how many now carry ONLY annotated introns / an annotated chain. usage: chain_diff.py a.bam b.bam annotation.bed12 label"""
import sys, pysam, collections
a, b, bed, label = sys.argv[1:5]
ann_introns, ann_chains = set(), set()
for ln in open(bed):
    f = ln.split("\t"); s = int(f[1]); sz = list(map(int, f[10].strip(",").split(","))); st = list(map(int, f[11].strip(",").split(",")))
    ch = tuple((f[0], s + st[i] + sz[i], s + st[i + 1]) for i in range(len(sz) - 1))
    ann_introns.update(ch); ann_chains.add(ch)
def chains(p):
    d = {}
    for r in pysam.AlignmentFile(p).fetch(until_eof=True):
        if r.is_unmapped or r.is_secondary or r.is_supplementary: continue
        pos = r.reference_start; ch = []
        for op, n in r.cigartuples:
            if op == 3: ch.append((r.reference_name, pos, pos + n)); pos += n
            elif op in (0, 2, 7, 8): pos += n
        d[r.query_name] = tuple(ch)
    return d
A, B = chains(a), chains(b)
chg = [q for q in A if q in B and A[q] != B[q]]
allann = lambda c: len(c) > 0 and all(j in ann_introns for j in c)
cnt = collections.Counter()
for q in chg:
    cnt["A_all_annotated" if allann(A[q]) else "A_has_novel"] += 1
    cnt["B_all_annotated" if allann(B[q]) else "B_has_novel"] += 1
    cnt["B_full_annotated_chain_subset"] += any(set(B[q]) <= set(c) for c in ann_chains) if B[q] else 0
print("%s: reads %d, chain changed %d (%.1f%%); before: %s ; after: %s" % (label, len(A), len(chg), 100.0 * len(chg) / len(A),
      {k: v for k, v in cnt.items() if k.startswith("A_")}, {k: v for k, v in cnt.items() if k.startswith("B_")}))
for q in chg[:6]:
    print("   ", q[:24], "default", [(x[1], x[2]) for x in A[q]][:6], "->", [(x[1], x[2]) for x in B[q]][:6])
