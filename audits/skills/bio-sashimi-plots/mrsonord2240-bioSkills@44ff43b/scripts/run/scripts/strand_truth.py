#!/usr/bin/env python3
"""Independent strand-aware junction count (pysam) for a dUTP-type library (MATE2_SENSE: read2 = sense).
Gene-strand of a read pair member: read2: '+' if forward else '-'; read1: '-' if forward else '+'.
For MATE1_SENSE it is the opposite. Prints {strand: {junction: n}} for BAM in region (1-based inclusive)."""
import sys, json, pysam
bam, chrom, s, e, mode = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
out = {'+': {}, '-': {}}
with pysam.AlignmentFile(bam) as f:
    for r in f.fetch(chrom, s - 1, e):
        if r.is_unmapped: continue
        rev = r.is_reverse
        if mode == 'MATE2_SENSE': st = ('+' if not rev else '-') if r.is_read2 else ('-' if not rev else '+')
        elif mode == 'MATE1_SENSE': st = ('+' if not rev else '-') if r.is_read1 else ('-' if not rev else '+')
        elif mode == 'SENSE': st = '-' if rev else '+'
        elif mode == 'ANTISENSE': st = '+' if rev else '-'
        pos = r.reference_start + 1
        for op, ln in r.cigartuples:
            if op == 3:
                d, a = pos, pos + ln
                if d > s - 1 and a < e:
                    k = f'{d}-{a}'; out[st][k] = out[st].get(k, 0) + 1
            if op in (0, 2, 3, 7, 8): pos += ln
print(json.dumps(out, sort_keys=True))
