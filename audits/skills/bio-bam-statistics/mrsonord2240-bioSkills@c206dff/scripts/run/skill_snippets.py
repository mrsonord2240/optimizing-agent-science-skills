#!/usr/bin/env python3
"""Python snippets copied VERBATIM (bodies unchanged) from bio-bam-statistics SKILL.md / usage-guide.md.
Only change: wrapped in functions taking the BAM path and printing, so they can be called from a test driver.
Each function is tagged with the doc location it came from.
"""
import pysam
from collections import Counter


def skill_count_reads(path):                      # SKILL.md "Count Reads"
    with pysam.AlignmentFile(path, 'rb') as bam:
        total = mapped = paired = proper = 0
        for read in bam:
            total += 1
            if not read.is_unmapped:
                mapped += 1
            if read.is_paired:
                paired += 1
            if read.is_proper_pair:
                proper += 1

        print(f'Total: {total}')
        print(f'Mapped: {mapped} ({mapped/total*100:.1f}%)')
        print(f'Properly paired: {proper} ({proper/paired*100:.1f}%)')
        return dict(total=total, mapped=mapped, paired=paired, proper=proper)


def skill_per_chrom(path):                        # SKILL.md "Per-Chromosome Counts"
    out = {}
    with pysam.AlignmentFile(path, 'rb') as bam:
        for stat in bam.get_index_statistics():
            print(f'{stat.contig}: {stat.mapped} mapped, {stat.unmapped} unmapped')
            out[stat.contig] = (stat.mapped, stat.unmapped)
    return out


def skill_depth_at(path, chrom, a, b):            # SKILL.md "Calculate Depth at Position"
    out = {}
    with pysam.AlignmentFile(path, 'rb') as bam:
        for pileup in bam.pileup(chrom, a, b):
            print(f'Position {pileup.pos}: depth {pileup.n}')
            out[pileup.pos] = pileup.n
    return out


def skill_mean_depth(bam_path, chrom, start, end):  # SKILL.md "Mean Depth in Region"
    depths = []
    with pysam.AlignmentFile(bam_path, 'rb') as bam:
        for pileup in bam.pileup(chrom, start, end, truncate=True):
            depths.append(pileup.n)

    if depths:
        return sum(depths) / len(depths)
    return 0


def skill_coverage_stats(bam_path, chrom, start, end):  # SKILL.md "Coverage Statistics"
    covered = 0
    total_depth = 0

    with pysam.AlignmentFile(bam_path, 'rb') as bam:
        for pileup in bam.pileup(chrom, start, end, truncate=True):
            covered += 1
            total_depth += pileup.n

    length = end - start
    pct_covered = covered / length * 100
    mean_depth = total_depth / length if length > 0 else 0

    return {
        'length': length,
        'covered_bases': covered,
        'pct_covered': pct_covered,
        'mean_depth': mean_depth
    }


def skill_insert_size(path):                      # SKILL.md "Insert Size Distribution"
    insert_sizes = Counter()

    with pysam.AlignmentFile(path, 'rb') as bam:
        for read in bam:
            if read.is_proper_pair and read.is_read1 and read.template_length > 0:
                insert_sizes[read.template_length] += 1

    sizes = list(insert_sizes.keys())
    mean_insert = sum(s * c for s, c in insert_sizes.items()) / sum(insert_sizes.values())
    print(f'Mean insert size: {mean_insert:.0f}')
    print(f'Min: {min(sizes)}, Max: {max(sizes)}')
    return mean_insert


def guide_flagstat(bam_path):                     # usage-guide.md "Flagstat Equivalent"
    stats = {'total': 0, 'mapped': 0, 'paired': 0, 'proper': 0, 'duplicate': 0}
    with pysam.AlignmentFile(bam_path, 'rb') as bam:
        for read in bam:
            stats['total'] += 1
            if not read.is_unmapped:
                stats['mapped'] += 1
            if read.is_paired:
                stats['paired'] += 1
            if read.is_proper_pair:
                stats['proper'] += 1
            if read.is_duplicate:
                stats['duplicate'] += 1
    stats['map_rate'] = stats['mapped'] / stats['total'] * 100
    return stats


def guide_region_coverage(bam_path, chrom, start, end):  # usage-guide.md "Coverage in Region"
    with pysam.AlignmentFile(bam_path, 'rb') as bam:
        depths = [0] * (end - start)
        for pileup in bam.pileup(chrom, start, end, truncate=True):
            if start <= pileup.pos < end:
                depths[pileup.pos - start] = pileup.n
    covered = sum(1 for d in depths if d > 0)
    mean_depth = sum(depths) / len(depths)
    return {'length': len(depths), 'covered': covered, 'pct_covered': covered / len(depths) * 100, 'mean_depth': mean_depth}
