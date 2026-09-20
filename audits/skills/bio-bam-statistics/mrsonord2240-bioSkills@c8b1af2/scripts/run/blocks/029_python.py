import pysam

def region_depth_stats(bam_path, chrom, start, end, thresholds=(10, 20), reference=None):
    """Depth over the 0-based half-open region [start, end); every base is in the denominator.
    A single position is the 1-bp region (pos - 1, pos). `reference` is the FASTA for a CRAM."""
    length = end - start
    if length <= 0:
        raise ValueError(f'empty region [{start}, {end})')
    depths = [0] * length
    with pysam.AlignmentFile(bam_path, 'rb', reference_filename=reference) as bam:
        # truncate=True: only columns inside the region (otherwise whole read footprints are returned)
        # max_depth: pysam's default cap is 8000; ignore_orphans=False: default drops paired reads
        #   that lack the proper-pair flag; min_base_quality=0: default is 13 (samtools depth: 0)
        # pileup.n counts deletions and ref-skips, so count real bases explicitly
        for col in bam.pileup(chrom, start, end, truncate=True, max_depth=1_000_000,
                              ignore_orphans=False, ignore_overlaps=False, min_base_quality=0):
            depths[col.reference_pos - start] = sum(1 for r in col.pileups if not r.is_del and not r.is_refskip)
    stats = {'length': length, 'covered': sum(d > 0 for d in depths),
             'mean_depth': sum(depths) / length, 'max_depth': max(depths)}
    stats['pct_covered'] = stats['covered'] / length * 100
    for t in thresholds:
        stats[f'pct_ge_{t}x'] = sum(d >= t for d in depths) / length * 100
    return stats

stats = region_depth_stats('input.bam', 'chr1', 1000000, 2000000)
print(f'Coverage: {stats["pct_covered"]:.1f}%  Mean depth: {stats["mean_depth"]:.1f}x  >=20x: {stats["pct_ge_20x"]:.1f}%')
