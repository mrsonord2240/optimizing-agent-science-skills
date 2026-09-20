samtools view /mnt/openscience/audits/bio-alignment-validation/run/data/idx/planted_lowmap_placed.bam | awk '{sum+=$5; count++} END {print "Mean MAPQ:", sum/count}'
