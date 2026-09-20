samtools view /mnt/openscience/audits/bio-alignment-validation/run/data/idx/real_human_PE.bam | cut -f5 | sort -n | uniq -c | sort -k2 -n
