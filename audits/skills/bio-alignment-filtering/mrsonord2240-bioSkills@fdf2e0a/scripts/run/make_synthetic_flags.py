#!/usr/bin/env python3
"""SYNTHETIC data: one read per FLAG value 0..4095 (all 12 SAM bits), MAPQ pseudo-cycled 0..60.
Real BAMs in public-data contain NO supplementary (2048) or QC-fail (512) reads, so exhaustive
flag arithmetic can only be checked on a synthetic set. Labelled synthetic; not real reads."""
import os, sys
import pysam

out = sys.argv[1]
hdr = {'HD': {'VN': '1.6', 'SO': 'unsorted'}, 'SQ': [{'SN': 'chr1', 'LN': 100000}],
       'RG': [{'ID': 'rg1', 'SM': 's'}]}
tmp = out + '.unsorted.bam'
with pysam.AlignmentFile(tmp, 'wb', header=hdr) as fo:
    for flag in range(4096):
        a = pysam.AlignedSegment(fo.header)
        a.query_name = f'f{flag}'
        a.flag = flag
        a.reference_id = 0
        a.reference_start = 1000 + (flag % 97) * 25
        a.mapping_quality = (flag * 7) % 61
        a.query_sequence = 'ACGT' * 5
        a.query_qualities = pysam.qualitystring_to_array('I' * 20)
        if not (flag & 4):
            a.cigartuples = [(0, 20)]
        a.set_tag('RG', 'rg1')
        fo.write(a)
pysam.sort('-o', out, tmp)
pysam.index(out)
os.remove(tmp)
n = sum(1 for _ in pysam.AlignmentFile(out))
assert n == 4096, n
print('wrote', out, n, 'records')
