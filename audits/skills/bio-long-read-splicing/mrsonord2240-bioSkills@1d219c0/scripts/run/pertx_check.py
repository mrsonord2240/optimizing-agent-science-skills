#!/usr/bin/env python3
"""Per-transcript exact-chain breakdown for a BAM (which transcripts lose their exact chain). usage: pertx_check.py bam truth_chains.tsv"""
import sys, collections, pysam
bam, truth = sys.argv[1:3]
ch = {}
for ln in list(open(truth))[1:]:
    f = ln.rstrip("\n").split("\t"); ch[f[0]] = tuple(tuple(map(int, j.split("-"))) for j in f[4].split(";")) if f[4] else ()
c = collections.defaultdict(collections.Counter); ex = {}
for r in pysam.AlignmentFile(bam).fetch(until_eof=True):
    if r.is_secondary or r.is_supplementary or r.is_unmapped: continue
    tx = r.query_name.split("_")[1]; pos = r.reference_start; obs = []
    for op, ln in r.cigartuples:
        if op == 3: obs.append((pos, pos + ln)); pos += ln
        elif op in (0, 2, 7, 8): pos += ln
    obs = tuple(obs); c[tx]["n"] += 1
    if obs == ch[tx]: c[tx]["exact"] += 1
    else: ex.setdefault(tx, collections.Counter())[obs] += 1
for tx, v in sorted(c.items()):
    print(tx, dict(v))
    if tx in ex:
        for o, n in ex[tx].most_common(2): print("   obs", n, o, " truth", ch[tx])
