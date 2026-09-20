#!/bin/bash
set -u
cd /mnt/openscience/audits/bio-pileup-generation/run/work/in04/par
rm -f chr*.vcf.gz* all.vcf.gz*
for chr in chr1 chr2 chr3 chr4 chr5 chr6 chr7 chr8 chr9 chr10 chr11; do
    bcftools mpileup -f /mnt/openscience/audits/bio-pileup-generation/run/data/multi.fa -r "$chr" -d 1000000 /mnt/openscience/audits/bio-pileup-generation/run/data/multi.bam | \
        bcftools call -mv -Oz -o "${chr}.vcf.gz" &
done
wait
bcftools concat -Oz -o all.vcf.gz chr*.vcf.gz && bcftools index all.vcf.gz
echo "concat_status=$?"
