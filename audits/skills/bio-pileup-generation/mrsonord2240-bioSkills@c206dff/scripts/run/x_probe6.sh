cd /mnt/openscience/audits/bio-pileup-generation/run/work/in04
bcftools mpileup -X list 2>&1 | sed -n 1,60p
echo ---; bcftools view -h par/all.vcf.gz | grep '##contig' | head -12
echo; bcftools view -h par/chr1.vcf.gz | grep -c '##contig'
H=/mnt/openscience/audit-envs/alignment-files/public-data/human
samtools mpileup -B -Q 20 -q 20 -f $H/genome.fasta -r chr22:3406-3406 $H/test.paired_end.sorted.bam | cut -f1-5 | cut -c1-200
bcftools mpileup -f $H/genome.fasta -d 1000000 -q 20 -Q 20 -a FORMAT/AD,FORMAT/DP -r chr22:3406 $H/test.paired_end.sorted.bam | bcftools call -m | grep -v '^##'
