# regtools 1.0.0: -s is required; 10X R2 reads are sense-strand, so -s RF. (-s XS writes strand '?' on BAMs without XS tags.)
regtools junctions extract -a 8 -m 50 -M 500000 -s RF -o junctions.bed possorted_genome_bam.bam
