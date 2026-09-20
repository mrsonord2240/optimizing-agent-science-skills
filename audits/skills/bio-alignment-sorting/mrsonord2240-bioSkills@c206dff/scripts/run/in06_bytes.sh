#!/bin/bash
# quick check: are BAM bytes identical across runs when @PG is suppressed? (T3 note)
source /mnt/openscience/audits/bio-alignment-sorting/run/common.sh
W=$WORK/in6; rm -rf $W; mkdir -p $W; cd $W
samtools sort --no-PG -o a.bam $DATA/shuffled_real.bam; samtools sort --no-PG -o b.bam $DATA/shuffled_real.bam
cmp -s a.bam b.bam && echo "byte-identical with --no-PG (different output names)" || echo "still differ"
samtools sort -o c.bam $DATA/shuffled_real.bam; samtools sort -o d.bam $DATA/shuffled_real.bam
cmp -s c.bam d.bam && echo "byte-identical with @PG, different names" || echo "differ with @PG (CL line has output name)"
