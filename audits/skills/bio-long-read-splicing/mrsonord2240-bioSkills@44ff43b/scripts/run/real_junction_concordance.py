#!/usr/bin/env python3
"""Second method on REAL long-read alignments: count distinct junctions carried by primary alignments (pysam CIGAR N)
and compare with (a) the reference annotation's introns and (b) short-read junctions (STAR SJ.out.tab-like) if given.
Usage: real_junction_concordance.py <bam> <annotation.gtf> [SJ.tab] [--collapse-bed12 <bed>]
"""
import sys, re, collections
import pysam

bam, gtf = sys.argv[1], sys.argv[2]
sj = sys.argv[3] if len(sys.argv) > 3 and not sys.argv[3].startswith("--") else None

ex = collections.defaultdict(list)
for ln in open(gtf):
    if ln.startswith("#"):
        continue
    f = ln.rstrip("\n").split("\t")
    if len(f) < 9 or f[2] != "exon":
        continue
    tid = re.search(r'transcript_id "([^"]+)"', f[8]).group(1)
    ex[tid].append((f[0], int(f[3]) - 1, int(f[4]), f[6]))
ann = set()
for tid, e in ex.items():
    e.sort(key=lambda x: x[1])
    for a, b in zip(e[:-1], e[1:]):
        ann.add((a[0], a[2], b[1], a[3]))
ann_nostrand = {(c, s, e) for c, s, e, _ in ann}
srj = set()
if sj:
    for ln in open(sj):
        f = ln.split("\t")
        # STAR SJ.out.tab: chr, first intron base (1-based), last intron base, strand(0/1/2), motif, annotated, uniq, multi, overhang
        srj.add((f[0], int(f[1]) - 1, int(f[2])))

sf = pysam.AlignmentFile(bam, "rb")
jn = collections.Counter()
n_aln = n_sp = 0
for r in sf.fetch(until_eof=True):
    if r.is_unmapped or r.is_secondary or r.is_supplementary:
        continue
    n_aln += 1
    pos = r.reference_start
    sp = False
    for op, ln in r.cigartuples:
        if op == 3:
            jn[(r.reference_name, pos, pos + ln)] += 1
            pos += ln
            sp = True
        elif op in (0, 2, 7, 8):
            pos += ln
    n_sp += sp
known = sum(1 for j in jn if j in ann_nostrand)
print("primary alignments %d ; spliced %d ; distinct junctions %d ; in annotation %d (%.1f%%)" % (n_aln, n_sp, len(jn), known, 100 * known / max(len(jn), 1)))
if srj:
    sr = sum(1 for j in jn if j in srj)
    print("distinct LR junctions also in short-read junction file: %d (%.1f%%); LR junctions unknown to annotation AND short reads: %d" % (
        sr, 100 * sr / max(len(jn), 1), sum(1 for j in jn if j not in ann_nostrand and j not in srj)))
reads_known = sum(c for j, c in jn.items() if j in ann_nostrand)
print("junction-observations %d ; on annotated junctions %d (%.1f%%)" % (sum(jn.values()), reads_known, 100 * reads_known / max(sum(jn.values()), 1)))
