#!/usr/bin/env python3
"""IsoQuant block (2 input files) per-sample counts (OUT.transcript_grouped_file_name_counts.tsv) vs planted truth: sample1 = ctrl1, sample2 = trt1."""
import csv, math, collections
D = "data/plant"
tc = collections.defaultdict(dict)
for r in list(csv.DictReader(open(D + "/hifi/truth_counts.tsv"), delimiter="\t")): tc[r["sample"]][r["transcript"]] = int(r["n_reads"])
rows = list(csv.reader(open("out/iq/isoquant_output/OUT/OUT.transcript_grouped_file_name_counts.tsv"), delimiter="\t"))
hdr = rows[0]; print("header:", hdr)
def pear(a, b):
    n = len(a); ma, mb = sum(a) / n, sum(b) / n
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / math.sqrt(sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b))
for k, s in ((1, "ctrl1"), (2, "trt1")):
    got = {r[0]: float(r[k]) for r in rows[1:] if not r[0].startswith("__")}
    tx = [t for t in tc[s] if t in got]
    print("%s: %d/%d truth transcripts present, Pearson r = %.4f, counted %.0f of %d truth reads; G001A truth %d got %.0f ; G001B truth %d got %.0f" % (
        s, len(tx), len(tc[s]), pear([tc[s][t] for t in tx], [got[t] for t in tx]), sum(got.values()), sum(tc[s].values()), tc[s]["G001A"], got["G001A"], tc[s]["G001B"], got["G001B"]))
