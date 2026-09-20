import pysam
from collections import Counter

insert_sizes = Counter()

with pysam.AlignmentFile('input.bam', 'rb') as bam:
    for read in bam:
        if read.is_secondary or read.is_supplementary or read.is_qcfail:
            continue
        if read.is_proper_pair and read.is_read1 and read.template_length > 0:
            insert_sizes[read.template_length] += 1

if not insert_sizes:
    raise SystemExit('no properly paired read1 records (single-end data, or proper-pair flag unset: see Insert Size Caveats)')
sizes = list(insert_sizes.keys())
mean_insert = sum(s * c for s, c in insert_sizes.items()) / sum(insert_sizes.values())
print(f'Mean insert size: {mean_insert:.0f}')
print(f'Min: {min(sizes)}, Max: {max(sizes)}')
