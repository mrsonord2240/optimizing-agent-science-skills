#!/usr/bin/env python3
"""flair diffSplice --test (DRIMSeq half) es-event results vs planted DTU truth. usage: eval_diffsplice.py <flair_diffsplice dir> [group1 group2 label]"""
import csv, sys, collections
d = sys.argv[1]
T = {r["gene"]: int(r["planted_dtu"]) for r in csv.DictReader(open("data/plant/truth_dtu.tsv"), delimiter="\t")}
ev = {r["feature_id"]: r["isoform_ids"] for r in csv.DictReader(open(d + "/diffsplice.es.events.quant.tsv"), delimiter="\t")}
res = list(csv.DictReader(open(d + "/drimseq_es_ctrl_v_trt.tsv"), delimiter="\t"))
sig = collections.defaultdict(float)
for r in res:
    g = ev[r["feature_id"]].split(",")[0].split("_")[-1]
    if r["adj_pvalue"] not in ("", "NA") and float(r["adj_pvalue"]) < 0.05: sig[g] = 1
plant = {g for g, v in T.items() if v}
print("ES events in quant table: %d ; tested by DRIMSeq (rows in result): %d ; genes with a significant ES event (adj p<0.05): %d" % (len(ev) // 2, len(res) // 2, len(sig)))
print("planted DTU genes recovered: %d/%d ; other genes called: %d %s" % (len(plant & set(sig)), len(plant), len(set(sig) - plant), sorted(set(sig) - plant)))
