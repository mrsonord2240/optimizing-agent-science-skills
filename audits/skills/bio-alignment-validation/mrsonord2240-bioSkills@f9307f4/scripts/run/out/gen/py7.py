import pysam
import numpy as np
import matplotlib.pyplot as plt

def get_insert_sizes(bam_file, max_reads=100000):
    sizes = []
    bam = pysam.AlignmentFile(bam_file, 'rb')
    for i, read in enumerate(bam.fetch(until_eof=True)):  # until_eof: no index needed
        if i >= max_reads:
            break
        if read.is_proper_pair and not read.is_secondary and read.template_length > 0:
            sizes.append(read.template_length)
    bam.close()
    return sizes

sizes = get_insert_sizes('/mnt/openscience/audit-envs/alignment-files/public-data/human/test.paired_end.umi_unsorted.bam')
print(f'Median insert size: {np.median(sizes):.0f}')
print(f'Mean insert size: {np.mean(sizes):.0f}')
print(f'Std dev: {np.std(sizes):.0f}')

plt.hist(sizes, bins=100, range=(0, 1000))
plt.xlabel('Insert Size')
plt.ylabel('Count')
plt.savefig('/dev/null', format='pdf')
