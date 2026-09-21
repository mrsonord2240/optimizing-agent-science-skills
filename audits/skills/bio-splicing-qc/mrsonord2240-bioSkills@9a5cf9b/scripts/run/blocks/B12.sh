total=$(samtools view -c -F 0x904 sample.bam)                       # -F 0x904: drop unmapped, secondary, supplementary
rrna=$(samtools view -c -F 0x904 -L rRNA_intervals.bed sample.bam)
awk -v r=$rrna -v t=$total 'BEGIN{printf "rRNA: %.1f%%\n", 100*r/t}'
