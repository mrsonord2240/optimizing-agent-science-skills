#!/usr/bin/env python3
"""rMATS-long ASM output vs planted DTU truth (data/plant/truth_dtu.tsv). usage: eval_rmatslong.py <rmats_long_output>"""
import csv, sys, collections
d = sys.argv[1]; T = {r["gene"]: int(r["planted_dtu"]) for r in csv.DictReader(open("data/plant/truth_dtu.tsv"), delimiter="\t")}
rows = list(csv.DictReader(open(d + "/differential_asms.tsv"), delimiter="\t"))
print("ASM rows", len(rows), "genes", len({r["gene_id"] for r in rows}))
for thr in (0.05, 0.01):
    called = {r["gene_id"] for r in rows if r["adj_pvalue"] not in ("", "NA") and float(r["adj_pvalue"]) < thr}
    tp = sum(T.get(g, 0) for g in called); fp = len(called) - tp
    print("adj_p < %s: genes called %d, planted DTU recovered %d/20, other genes called %d" % (thr, len(called), tp, fp))
tested = {r["gene_id"] for r in rows}
print("planted DTU genes tested by rMATS-long:", sum(1 for g in T if T[g] and g in tested), "/20")
