#!/usr/bin/env python3
"""Compare skera S-reads (segmented BAM) with the planted segments. Sequences are compared up to reverse complement (skera may reorient)."""
import pysam, sys, collections
comp = str.maketrans("ACGT", "TGCA"); rc = lambda s: s.translate(comp)[::-1]
truth = [ln.rstrip("\n").split("\t") for ln in open("truth3.tsv")][1:]
segs = collections.defaultdict(set)
for z, k, s in truth:
    for x in s.split(","): segs[z].add(x); segs[z].add(rc(x))
got = collections.defaultdict(list)
for r in pysam.AlignmentFile(sys.argv[1], check_sq=False):
    z = r.query_name.split("/")[1]; got[z].append((r.query_sequence, r.get_tag("dl") if r.has_tag("dl") else None, r.get_tag("dr") if r.has_tag("dr") else None))
tot = ok = 0; byk = collections.defaultdict(lambda: [0, 0, 0])
for z, k, s in truth:
    exp = s.split(","); g = got.get(z, [])
    m = sum(1 for x in g if x[0] in segs[z])
    byk[k][0] += len(exp); byk[k][1] += len(g); byk[k][2] += m
print("kind: expected S-reads / skera S-reads / S-reads whose sequence equals a planted segment (either strand)")
for k, v in byk.items(): print("  %-24s %3d / %3d / %3d" % (k, *v))
print("total S-reads in BAM:", sum(len(v) for v in got.values()), "; example dl/dr of zmw 1:", [(x[1], x[2]) for x in got["1"]])
