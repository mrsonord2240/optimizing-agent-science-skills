bcftools --version | head -1
printf 'chr1\t5000\t9000\nchr1\t8000\t12000\n' > overlap.bed
printf 'chr1\t8000\t12000\nchr1\t5000\t9000\n' > overlap_unsorted.bed
for b in overlap.bed overlap_unsorted.bed; do echo "$b -R: $(bcftools view -H -R $b cohort.vcf.gz | wc -l) distinct $(bcftools view -H -R $b cohort.vcf.gz | cut -f1-5 | sort -u | wc -l)"; done
echo "regions-overlap 1 (default) vs 2:"; bcftools view -H -R overlap.bed --regions-overlap 2 cohort.vcf.gz | wc -l
