#!/usr/bin/env python3
"""IsoQuant transcript_counts.tsv vs truth on data/micro2 (150 reads per isoform). Prints, over the 12 single-microexon genes, mean counted inclusion (xinc) and skipping (xskip) reads out of 150, and the tandem genes."""
import sys
f, truth, label = sys.argv[1:4]
c = {}
for ln in open(f):
    if ln.startswith("#") or ln.startswith("feature_id"): continue
    a, b = ln.rstrip("\n").split("\t")[:2]; c[a] = float(b)
gs = ["M%02d" % i for i in range(1, 13)]
inc = [c.get(g + "inc", 0) for g in gs]; skp = [c.get(g + "skip", 0) for g in gs]
print("  %-16s inclusion isoform counted: mean %.1f/150 (min %d, %d of 12 genes below 135) | skipping isoform: mean %.1f/150 (min %d) | T1 inc %d skip %d, T2 inc %d skip %d | __ambiguous %d" % (
    label, sum(inc) / 12, min(inc), sum(x < 135 for x in inc), sum(skp) / 12, min(skp), c.get("T1inc", 0), c.get("T1skip", 0), c.get("T2inc", 0), c.get("T2skip", 0), c.get("__ambiguous", 0)))
