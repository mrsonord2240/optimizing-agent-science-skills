#!/bin/bash
# Input 5: convert, index, region query, gzip-vs-bgzip failure, Python filtered write.
set -uo pipefail
bcftools view -Ob -o cohort.bcf ../../data/cohort.vcf && bcftools index cohort.bcf
bgzip -c ../../data/cohort.vcf > cohort.vcf.gz && bcftools index -t cohort.vcf.gz
ls -l cohort.bcf cohort.vcf.gz | awk '{print $5, $9}'
echo "== region query chr2:1-3000 on BCF =="; bcftools view -H cohort.bcf chr2:1-3000 | wc -l
gzip -c ../../data/cohort.vcf > plain_gzip.vcf.gz
echo "== region query on a plain-gzip file =="; bcftools index plain_gzip.vcf.gz 2>&1 | tail -2; bcftools view -H plain_gzip.vcf.gz chr2:1-3000 2>&1 | tail -2
