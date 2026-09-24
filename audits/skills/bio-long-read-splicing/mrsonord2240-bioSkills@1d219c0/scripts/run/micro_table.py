#!/usr/bin/env python3
"""One line per microexon gene: inclusion reads that keep the microexon (carry both flanking junctions) / N,
and skipping reads whose alignment is exactly the skip chain (a control: a rescue must not force inclusion). usage: micro_table.py bam truth_chains.tsv label"""
import sys, collections, pysam
bam, truth, label = sys.argv[1:4]
ch = {}
for ln in list(open(truth))[1:]:
    f = ln.rstrip("\n").split("\t"); ch[f[0]] = tuple(tuple(map(int, j.split("-"))) for j in f[4].split(";"))
inc, skip = collections.Counter(), collections.Counter()
for r in pysam.AlignmentFile(bam).fetch(until_eof=True):
    if r.is_secondary or r.is_supplementary or r.is_unmapped: continue
    tx = r.query_name.split("_")[1]; pos = r.reference_start; obs = []
    for op, ln in r.cigartuples:
        if op == 3: obs.append((pos, pos + ln)); pos += ln
        elif op in (0, 2, 7, 8): pos += ln
    obs = tuple(obs); g = tx[:-3] if tx.endswith("inc") else tx[:-4]
    if tx.endswith("inc"):
        inc[g + "n"] += 1
        if ch[tx][0] in obs and ch[tx][1] in obs: inc[g] += 1
    else:
        skip[g + "n"] += 1
        if obs == ch[tx]: skip[g] += 1
gs = sorted({k[:-1] for k in inc if k.endswith("n")} , key=lambda x: (len(x), x))
print("%-34s" % label + " ".join("%s inc %3d/%d skip %3d/%d |" % (g, inc[g], inc[g + "n"], skip[g], skip[g + "n"]) for g in gs))
