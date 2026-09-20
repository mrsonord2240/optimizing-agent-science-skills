#!/usr/bin/env python3
"""Does an IsoQuant output contain a model whose intron chain equals the planted novel isoforms G057N / G058N? and their counts. usage: iq_novel_check.py <isoquant dir/prefix dir> <prefix> <sample>"""
import sys, re, os, collections
d, prefix = sys.argv[1:3]
HERE = os.path.dirname(os.path.abspath(__file__)); D = HERE + "/data/plant"
truth = {}
for ln in list(open(D + "/truth_chains.tsv"))[1:]:
    f = ln.rstrip("\n").split("\t"); truth[f[0]] = tuple(tuple(map(int, j.split("-"))) for j in f[4].split(";"))
ex = collections.defaultdict(list)
for ln in open(os.path.join(d, prefix + ".transcript_models.gtf")):
    f = ln.rstrip("\n").split("\t")
    if len(f) > 8 and f[2] == "exon":
        ex[re.search(r'transcript_id "([^"]+)"', f[8]).group(1)].append((int(f[3]) - 1, int(f[4])))
chains = {t: tuple((sorted(e)[i][1], sorted(e)[i + 1][0]) for i in range(len(e) - 1)) for t, e in ex.items()}
cnt = {}
for fn in (".transcript_counts.tsv", ".discovered_transcript_counts.tsv"):
    p = os.path.join(d, prefix + fn)
    if os.path.exists(p):
        for ln in open(p):
            if not ln.startswith(("#", "feature_id")): a, b = ln.split("\t")[:2]; cnt[a] = float(b)
for nov in ("G057N", "G058N"):
    hit = [t for t, c in chains.items() if c == truth[nov]]
    print("  planted %s: models with its exact chain: %s ; count %s" % (nov, hit, [cnt.get(t) for t in hit]))
