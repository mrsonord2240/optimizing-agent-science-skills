H=/mnt/openscience/audit-envs/alignment-files/public-data/human
cd /mnt/openscience/audits/bio-pileup-generation/run/work
samtools mpileup -f $H/genome.fasta -l t.bed $H/test.paired_end.sorted.bam | cut -f1-4
printf 'chr22\t3099\t3101\nchr22\t2999\t3003\n' > t2.bed
echo --- reversed order; samtools mpileup -f $H/genome.fasta -l t2.bed $H/test.paired_end.sorted.bam | cut -f1-4
printf 'chr22\t3100\nchr22\t3000\n' > t3.txt; echo --- pos file; samtools mpileup -f $H/genome.fasta -l t3.txt $H/test.paired_end.sorted.bam | cut -f1-4
echo --- -r + -l;  samtools mpileup -f $H/genome.fasta -r chr22:3000-3200 -l t.bed $H/test.paired_end.sorted.bam | cut -f1-4
samtools depth -a -r chr22:3095-3105 $H/test.paired_end.sorted.bam
