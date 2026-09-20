computeGCBias \
    -b /mnt/openscience/audit-envs/alignment-files/public-data/human/test.paired_end.sorted.bam \
    --effectiveGenomeSize 40001 \
    -g /mnt/openscience/audit-envs/alignment-files/public-data/human/genome.2bit \
    -o gc_bias.txt \
    --biasPlot gc_bias.pdf
