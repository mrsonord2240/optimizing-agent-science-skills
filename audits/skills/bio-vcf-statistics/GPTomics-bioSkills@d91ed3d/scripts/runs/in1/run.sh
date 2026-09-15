#!/bin/bash
# Input 1 (Canonical): "Give me a QC summary of cohort.vcf: counts, Ti/Tv, per-sample het/hom and missingness,
# and tell me whether the callset looks trustworthy." SYNTHETIC 8-sample raw joint callset (data/make_data.py):
# SYN_S6 low coverage, SYN_S7 contaminated, SYN_S8 re-sequenced duplicate of SYN_S3, 70 artifact sites.
set -uo pipefail
source ../env.sh
S=../../data
bgzip -c $S/cohort.vcf > cohort.vcf.gz; bcftools index -t -f cohort.vcf.gz
echo "### $(bcftools --version | head -1)"
bcftools stats cohort.vcf.gz > stats.txt              # SKILL.md: cohort-level
bcftools stats -s - cohort.vcf.gz > per_sample.txt    # SKILL.md: per-sample (PSC/PSI lines)
echo "== SN (grep ^SN | cut -f3-) =="; grep "^SN" stats.txt | cut -f3-
echo "== TSTV header + line; SKILL.md says ratio is field 5 =="; grep "^# TSTV" stats.txt; grep "^TSTV" stats.txt
echo "cut -f5 -> $(grep '^TSTV' stats.txt | cut -f5)"
echo "== PSC header + lines =="; grep "^# PSC" per_sample.txt; grep "^PSC" per_sample.txt
echo "== usage-guide missingness idiom: grep ^PSC | cut -f3,14 =="; grep "^PSC" per_sample.txt | cut -f3,14
echo "== derived per-sample het/hom-alt ratio =="; grep "^PSC" per_sample.txt | awk -F'\t' '{printf "%s het=%d homalt=%d het/hom=%.2f missing=%d\n",$3,$6,$5,($5>0?$6/$5:0),$14}'
echo "== quick counts (SKILL.md) =="
echo "records $(bcftools view -H cohort.vcf.gz | wc -l) snps $(bcftools view -v snps -H cohort.vcf.gz | wc -l) indels $(bcftools view -v indels -H cohort.vcf.gz | wc -l) PASS $(bcftools view -f PASS -H cohort.vcf.gz | wc -l)"
bcftools query -f '%QUAL\n' cohort.vcf.gz | awk '{s+=$1;n++} END{print "mean QUAL:", s/n}'
git -C F:/OpenScience/external/GPTomics__bioSkills show HEAD:variant-calling/vcf-statistics/examples/vcf_stats.py > vcf_stats.upstream_copy.py
echo "== shipped examples/vcf_stats.py and plot-vcfstats: WSL, see out_wsl.txt =="
