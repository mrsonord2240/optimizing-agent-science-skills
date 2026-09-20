samtools view /mnt/openscience/audits/bio-alignment-validation/run/data/idx/real_human_PE.bam | awk '{sum+=$5; count++} END {print "Mean MAPQ:", sum/count}'
