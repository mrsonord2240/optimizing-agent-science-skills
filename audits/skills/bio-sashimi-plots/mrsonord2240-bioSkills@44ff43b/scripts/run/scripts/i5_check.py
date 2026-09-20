#!/usr/bin/env python3
"""Input 5 assertions on the REAL ENCODE 10-BAM ggsashimi example (chr10:27040584-27048100).
(a) ggsashimi -j per-sample junction BED (-M 10) == independent pysam per-read counts (>=10) incl. 1-based coordinates.
(b) aggregate labels in SVG (-O 3 -A mean_j -M 10) == round(mean) over samples of the group that pass -M, computed independently.
Usage: i5_check.py <tsv> <truth.json> <bed> <svg>"""
import sys, json, csv, re, collections
import xml.etree.ElementTree as ET
tsv, truth_p, bed_p, svg_p = sys.argv[1:5]
truth = json.load(open(truth_p))
rows = [l.rstrip('\n').split('\t') for l in open(tsv)]
id2bam = {r[0]: r[1].split('/')[-1] for r in rows}
id2grp = {r[0]: r[2] for r in rows}
M = 10
# (a)
bed = collections.defaultdict(dict)
for l in open(bed_p):
    c, s, e, sid, n, st = l.rstrip('\n').split('\t')
    bed[sid][f"{s}-{e}"] = int(n)
ok = True; nj = 0
for sid, bam in id2bam.items():
    exp = {k: v for k, v in truth[bam].items() if v >= M}
    got = bed.get(sid, {})
    if exp != got:
        ok = False; print('MISMATCH', sid, 'expected', exp, 'got', got)
    nj += len(exp)
print(f'(a) per-sample junction BED == pysam (>= {M}): {ok}  ({nj} sample-junction pairs, {len(id2bam)} samples)')
# (b)
def rnd(x):  # R round(): half to even, same as python round
    return int(round(x))
exp_labels = []
for g in sorted(set(id2grp.values())):
    keys = set()
    for sid, bam in id2bam.items():
        if id2grp[sid] == g: keys |= set(truth[bam])
    for k in keys:
        vals = [truth[id2bam[sid]].get(k, 0) for sid in id2bam if id2grp[sid] == g]
        kept = [v for v in vals if v >= M]
        if kept:
            exp_labels.append((g, k, rnd(sum(kept) / len(kept)), rnd(sum(vals) / len(vals))))
t = ET.parse(svg_p)
texts = collections.Counter(''.join(el.itertext()).strip() for el in t.iter() if el.tag.endswith('text'))
miss = [x for x in exp_labels if texts[str(x[2])] == 0]
print('(b) expected aggregate labels (group, junction, mean-of-kept, true-mean-all-samples):')
for x in sorted(exp_labels): print('   ', x, 'IN SVG' if texts[str(x[2])] else 'MISSING')
print('(b) all expected labels present in SVG:', not miss)
diff = [x for x in exp_labels if x[2] != x[3]]
print('(b) labels where filter-before-aggregate differs from true mean of all samples:', diff)
