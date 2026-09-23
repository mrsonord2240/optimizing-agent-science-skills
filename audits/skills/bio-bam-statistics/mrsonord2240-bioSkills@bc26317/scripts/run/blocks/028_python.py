import pysam

with pysam.AlignmentFile('input.bam', 'rb') as bam:
    # needs an index (ValueError otherwise); counts include secondary/supplementary like idxstats
    for stat in bam.get_index_statistics():
        print(f'{stat.contig}: {stat.mapped} mapped, {stat.unmapped} unmapped')
