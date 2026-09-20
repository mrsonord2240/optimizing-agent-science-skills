import pysam

with pysam.AlignmentFile('/mnt/openscience/audits/bio-bam-statistics/run/data/noindex.bam', 'rb') as bam:
    # needs an index (ValueError otherwise); counts include secondary/supplementary like idxstats
    for stat in bam.get_index_statistics():
        print(f'{stat.contig}: {stat.mapped} mapped, {stat.unmapped} unmapped')
