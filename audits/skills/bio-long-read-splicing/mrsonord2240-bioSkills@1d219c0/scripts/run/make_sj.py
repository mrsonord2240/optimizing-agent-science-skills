#!/usr/bin/env python3
"""STAR-layout SJ.out.tab (chr, intron first 1-based, intron last 1-based, strand 0/1/2, motif, annotated, unique, multi, overhang) from the
planted truth chains (all isoforms incl. the 2 novel ones) = an idealised short-read junction file. usage: make_sj.py truth_chains.tsv chr out"""
import sys
tr, chrom, out = sys.argv[1:4]
sj = set()
for ln in list(open(tr))[1:]:
    f = ln.rstrip("\n").split("\t")
    st = 1 if f[2] == "+" else 2
    for j in f[4].split(";"):
        a, b = map(int, j.split("-"))       # half-open 0-based (first intron base, first base of next exon)
        sj.add((a + 1, b, st))              # 1-based first / last intron base
with open(out, "w") as fh:
    for a, b, st in sorted(sj):
        fh.write("%s\t%d\t%d\t%d\t%d\t0\t40\t0\t40\n" % (chrom, a, b, st, st))
print(len(sj), "junctions ->", out)
