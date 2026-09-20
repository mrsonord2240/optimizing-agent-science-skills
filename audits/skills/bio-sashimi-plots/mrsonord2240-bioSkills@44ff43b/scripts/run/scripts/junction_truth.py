#!/usr/bin/env python3
"""Independent junction counter (pysam). Counts every read (per-read, primary+secondary excluded by default flag filter none)
that has an N CIGAR op inside region. Output JSON {bam_stem: {"donor_1based-acceptor_1based": count}}.
Coordinates: donor = first intron base (1-based), acceptor = first base of next exon (1-based) == ggsashimi's (don, acc) key.
Usage: junction_truth.py chrom start end bam1 [bam2 ...]  (start/end 1-based inclusive, like ggsashimi -c)
"""
import sys, json, os, pysam
chrom, s, e = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
out = {}
for bam in sys.argv[4:]:
    d = {}
    with pysam.AlignmentFile(bam) as f:
        for r in f.fetch(chrom, s - 1, e):
            if r.is_unmapped:
                continue
            pos = r.reference_start + 1
            for op, ln in r.cigartuples:
                if op == 3:
                    don, acc = pos, pos + ln
                    if don > s - 1 and acc < e:
                        k = f"{don}-{acc}"
                        d[k] = d.get(k, 0) + 1
                if op in (0, 2, 3, 7, 8):
                    pos += ln
    out[os.path.basename(bam)] = d
print(json.dumps(out, indent=1, sort_keys=True))
