computeGCBias \
    -b /mnt/openscience/audits/bio-alignment-validation/run/data/idx/real_human_PE.bam \
    --effectiveGenomeSize 2913022398 \
    -g /mnt/openscience/audit-envs/alignment-files/public-data/human/genome.2bit \
    -o gc_bias.txt \
    --biasPlot gc_bias.pdf
