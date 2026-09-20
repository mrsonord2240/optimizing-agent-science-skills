samtools depth -a -r chr22:1-40001 input.bam                              # 10 Mb region
samtools view -s 42.1 -b -o sub.bam input.bam && samtools depth -a sub.bam
