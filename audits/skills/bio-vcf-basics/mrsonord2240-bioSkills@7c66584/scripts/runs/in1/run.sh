#!/bin/bash
# Input 1 (canonical): inspect callerA.vcf -- header, samples, tabular extract, SNP/indel counts.
set -uo pipefail
bgzip -c ../../data/callerA.vcf > callerA.vcf.gz; bcftools index -t callerA.vcf.gz
echo "== header INFO/FORMAT lines =="; bcftools view -h callerA.vcf.gz | grep -E '^##(INFO|FORMAT|contig)'
echo "== samples =="; bcftools query -l callerA.vcf.gz
echo "== query with -H (SKILL.md: 'column header') =="
bcftools query -H -f '%CHROM\t%POS\t%REF\t%ALT\t%QUAL[\t%GT\t%GQ\t%AD]\n' callerA.vcf.gz | head -4
echo "== counts =="; echo "SNPs: $(bcftools view -v snps -H callerA.vcf.gz | wc -l)  indels: $(bcftools view -v indels -H callerA.vcf.gz | wc -l)  total: $(bcftools view -H callerA.vcf.gz | wc -l)"
bcftools query -f '%TYPE\n' callerA.vcf.gz | sort | uniq -c
