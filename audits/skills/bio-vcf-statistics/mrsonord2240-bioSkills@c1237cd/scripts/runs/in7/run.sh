#!/bin/bash
# Input 7 (NEW, re-audit 2026-09-15, Variant C): "How many variants passed filters in our raw joint callset (FILTER is '.'
# everywhere) and in the soft-filtered copy with LowQual labels? Give me the number from bcftools and from your Python script,
# and tell me why they differ if they do." Windows bcftools 1.24 part; the example (cyvcf2) runs in WSL: run_wsl.sh.
set -uo pipefail
source ../env.sh
S=../../data
bgzip -c $S/cohort.vcf > cohort.vcf.gz; bcftools index -f cohort.vcf.gz
bcftools filter -s LowQual -e 'QUAL<30' cohort.vcf.gz -Oz -o marked.vcf.gz; bcftools index -f marked.vcf.gz
git -C F:/OpenScience/external/mrsonord2240__bioSkills show c1237cdbc9bb199947696f3909de26a55d259116:variant-calling/vcf-statistics/examples/vcf_stats.py > vcf_stats.fork_copy.py
for f in cohort marked; do
  echo "== $f: FILTER values $(bcftools query -f '%FILTER\n' $f.vcf.gz | tr -d '\r' | sort | uniq -c | tr '\n' ' ')"
  echo "SKILL.md quick count 'bcftools view -f PASS -H | wc -l': $(bcftools view -f PASS -H $f.vcf.gz | wc -l)"
  echo "bcftools view -f .,PASS -H | wc -l: $(bcftools view -f .,PASS -H $f.vcf.gz | wc -l)"
done
grep -n "PASS\|FILTER" vcf_stats.fork_copy.py | head -8
