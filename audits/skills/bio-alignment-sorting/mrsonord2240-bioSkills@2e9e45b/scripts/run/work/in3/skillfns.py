import pysam

def is_coordinate_sorted(path):
    """True only if the records really are in (reference order, POS) order, fully unmapped reads last."""
    with pysam.AlignmentFile(path, 'rb') as bam:
        prev = (-1, -1)
        for r in bam.fetch(until_eof=True):
            key = (r.reference_id if r.reference_id >= 0 else float('inf'), r.reference_start)
            if key < prev:
                return False
            prev = key
    return True

def ensure_coordinate_sorted(input_bam, output_bam):
    if is_coordinate_sorted(input_bam):
        return input_bam
    pysam.sort('-o', output_bam, input_bam)
    return output_bam
