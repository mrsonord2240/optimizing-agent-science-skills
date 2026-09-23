samtools depth -a input.bam > depth_with_zeros.txt     # all positions of contigs that have reads
samtools depth -aa input.bam > depth_all_contigs.txt   # every position of every @SQ contig
