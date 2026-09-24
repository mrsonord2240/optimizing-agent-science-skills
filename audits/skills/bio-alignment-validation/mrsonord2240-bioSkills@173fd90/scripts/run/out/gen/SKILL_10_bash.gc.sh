picard CollectGcBiasMetrics \
    I=/mnt/openscience/audit-envs/alignment-files/public-data/human/test.paired_end.sorted.bam \
    O=gc_bias_metrics.txt \
    CHART=gc_bias_chart.pdf \
    S=gc_summary.txt \
    R=/mnt/openscience/audit-envs/alignment-files/public-data/human/genome.fasta
