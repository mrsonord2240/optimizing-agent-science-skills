#!/usr/bin/env python3
"""SQANTI3 classification of the planted FLAIR isoforms (out/hifi6) against truth. FLAIR names novel isoforms <sample>_<TX>_<n>_<gene>, annotated ones <TX>_<gene>.
Expected: every annotated truth isoform full-splice_match, G057N novel_in_catalog, G058N novel_not_in_catalog."""
import csv, collections, re
rows = list(csv.DictReader(open("sqanti3_qc/sqanti3_classification.txt"), delimiter="\t"))
def tx(i):
    m = re.search(r"(G\d{3}[ABCN])", i); return m.group(1)
cat = {tx(r["isoform"]): (r["structural_category"], r["subcategory"]) for r in rows}
fsm = sum(1 for t, (c, s) in cat.items() if not t.endswith("N") and c == "full-splice_match")
print("isoforms classified:", len(rows), dict(collections.Counter(c for c, s in cat.values())))
print("annotated truth isoforms -> full-splice_match: %d/%d" % (fsm, sum(1 for t in cat if not t.endswith("N"))))
print("G057N (novel exon-skip of known junctions):", cat.get("G057N"), " expected novel_in_catalog")
print("G058N (novel 5'ss, +30 nt):", cat.get("G058N"), " expected novel_not_in_catalog")
