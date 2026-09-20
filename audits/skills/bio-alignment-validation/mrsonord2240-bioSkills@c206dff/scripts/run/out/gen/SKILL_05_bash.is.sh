samtools stats /mnt/openscience/audits/bio-alignment-validation/run/data/idx/real_human_PE.bam > stats.txt
grep "^IS" stats.txt | cut -f2,3 > insert_sizes.txt
