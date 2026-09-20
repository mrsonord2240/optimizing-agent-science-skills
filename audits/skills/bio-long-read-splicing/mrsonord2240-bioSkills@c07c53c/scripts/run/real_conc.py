#!/usr/bin/env python3
"""Second method on real reads: fraction of spliced primary alignments whose junctions are ALL annotated introns (pysam vs the GTF), and total junction observations.
usage: real_conc.py <bam> <gtf>"""
import sys, re, collections, pysam
bam, gtf = sys.argv[1:3]
ex = collections.defaultdict(list)
for ln in open(gtf):
    if ln.startswith("#"): continue
    f = ln.rstrip("\n").split("\t")
    if len(f) > 8 and f[2] == "exon":
        ex[re.search(r'transcript_id "([^"]+)"', f[8]).group(1)].append((int(f[3]) - 1, int(f[4])))
ann = set()
for t, e in ex.items():
    e.sort(); ann.update((e[i][1], e[i + 1][0]) for i in range(len(e) - 1))
n = allann = jn = jann = 0
for r in pysam.AlignmentFile(bam).fetch(until_eof=True):
    if r.is_unmapped or r.is_secondary or r.is_supplementary: continue
    pos = r.reference_start; js = []
    for op, ln in r.cigartuples:
        if op == 3: js.append((pos, pos + ln)); pos += ln
        elif op in (0, 2, 7, 8): pos += ln
    if not js: continue
    n += 1; jn += len(js); k = sum(1 for j in js if j in ann); jann += k; allann += (k == len(js))
print("spliced primary reads %d ; all junctions annotated: %d (%.1f%%) ; junction observations %d, annotated %d (%.1f%%)" % (n, allann, 100 * allann / max(n, 1), jn, jann, 100 * jann / max(jn, 1)))
