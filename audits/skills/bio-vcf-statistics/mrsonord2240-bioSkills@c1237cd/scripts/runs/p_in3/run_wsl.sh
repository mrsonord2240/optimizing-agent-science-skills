#!/bin/bash
set -uo pipefail
cd "$(dirname "$0")"
export PATH=/tmp/vaca/env/bin:$PATH
S=../../data
echo "== SKILL.md: vcftools --gzvcf controls.vcf.gz --hardy --out hwe (exact test) =="
vcftools --gzvcf gtf.vcf.gz --hardy --out hwe > hwe.log 2>&1; echo "exit=$?"
head -2 hwe.hwe
echo "sites P_HWE<0.01: $(awk 'NR>1 && $6<0.01' hwe.hwe | wc -l); P_HET_EXCESS<0.01: $(awk 'NR>1 && $8<0.01' hwe.hwe | wc -l); P_HET_DEFICIT<0.01: $(awk 'NR>1 && $7<0.01' hwe.hwe | wc -l)"
awk 'NR>1 && $8<0.01 {print $1"\t"$2}' hwe.hwe > excess.tsv
echo "excess-het (vcftools) by truth class:"; awk -F'\t' 'NR==FNR{c[$1"\t"$2]=$3;next} {print c[$1"\t"$2]}' $S/cohort_truth_classes.tsv excess.tsv | sort | uniq -c
