#!/bin/bash
set -uo pipefail
cd "$(dirname "$0")"
export PATH=/tmp/vaca/env/bin:$PATH
echo "== SKILL.md: vcftools --gzvcf input.vcf.gz --missing-indv / --missing-site =="
vcftools --gzvcf cohort.vcf.gz --missing-indv --out sample_miss > m1.log 2>&1; echo "exit=$?"; cat sample_miss.imiss
vcftools --gzvcf cohort.vcf.gz --missing-site --out site_miss > m2.log 2>&1; echo "exit=$?"; echo "sites with F_MISS>0.05: $(awk 'NR>1 && $6>0.05' site_miss.lmiss | wc -l)"
