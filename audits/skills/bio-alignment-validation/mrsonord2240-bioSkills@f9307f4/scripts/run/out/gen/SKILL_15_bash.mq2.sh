samtools view -F 2308 /mnt/openscience/audit-envs/alignment-files/public-data/human/test.paired_end.sorted.bam | awk '{sum+=$5; count++} END {if (count) print "Mean MAPQ:", sum/count}'
