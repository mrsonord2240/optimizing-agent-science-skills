samtools idxstats /mnt/openscience/audits/bio-alignment-validation/run/data/idx/real_human_PE.bam | awk '{print $1, $3/$2}' | head -25
