import pysam
from collections import defaultdict

def junction_stats(bam_path):
    bam = pysam.AlignmentFile(bam_path, 'rb')
    counts = defaultdict(int)
    min_overhang = defaultdict(lambda: float('inf'))

    for read in bam.fetch():
        if read.is_unmapped or read.is_secondary:
            continue
        ref_pos = read.reference_start
        cumulative_query = 0
        cigar = read.cigartuples
        for i, (op, length) in enumerate(cigar):
            if op == 3:
                left_match = sum(l for o, l in cigar[:i] if o in (0, 7, 8))
                right_match = sum(l for o, l in cigar[i+1:] if o in (0, 7, 8))
                overhang = min(left_match, right_match)
                key = (read.reference_name, ref_pos, ref_pos + length)
                counts[key] += 1
                min_overhang[key] = min(min_overhang[key], overhang)
            if op in (0, 2, 3, 7, 8):
                ref_pos += length

    bam.close()
    return counts, dict(min_overhang)
