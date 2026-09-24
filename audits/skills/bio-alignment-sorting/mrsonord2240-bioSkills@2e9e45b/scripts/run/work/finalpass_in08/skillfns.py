import pysam

def is_coordinate_sorted(path, reference_filename=None):
    """True only if records are in (reference order, POS) order, with unmapped reads last."""
    with pysam.AlignmentFile(path, 'rb', check_sq=False,
                             reference_filename=reference_filename) as bam:
        if not bam.references:       # uBAM has no coordinate order to verify
            return False
        prev = (-1, -1)
        for r in bam.fetch(until_eof=True):
            key = (r.reference_id, r.reference_start) if r.reference_id >= 0 else (float('inf'), float('inf'))
            if key < prev:
                return False
            prev = key
    return True

def ensure_coordinate_sorted(input_bam, output_bam, reference_filename=None):
    if is_coordinate_sorted(input_bam, reference_filename):
        return input_bam
    pysam.sort('-o', output_bam, input_bam)
    return output_bam
