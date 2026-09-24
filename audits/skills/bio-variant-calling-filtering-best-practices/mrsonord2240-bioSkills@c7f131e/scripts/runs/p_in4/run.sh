#!/bin/bash
# Input 4 (Variant B): "Null out low-confidence genotypes before I compute per-sample missingness and HWE
# on the cohort." Site filter -> genotype filter (SKILL.md verbatim) -> recompute cohort metrics. SYNTHETIC data.
set -uo pipefail
source ../env.sh
S=../../data
bgzip -c $S/cohort.vcf > cohort.vcf.gz; bcftools index -f cohort.vcf.gz
bcftools filter -i '(TYPE="snp" && QUAL>=30 && (INFO/QD>=2.0||INFO/QD=".") && (INFO/FS<=60.0||INFO/FS=".") && (INFO/MQ>=40.0||INFO/MQ=".") && (INFO/MQRankSum>=-12.5||INFO/MQRankSum=".") && (INFO/ReadPosRankSum>=-8.0||INFO/ReadPosRankSum=".") && (INFO/SOR<=3.0||INFO/SOR=".")) || (TYPE="indel" && QUAL>=30 && (INFO/QD>=2.0||INFO/QD=".") && (INFO/FS<=200.0||INFO/FS=".") && (INFO/ReadPosRankSum>=-20.0||INFO/ReadPosRankSum=".") && (INFO/SOR<=10.0||INFO/SOR="."))' cohort.vcf.gz -Oz -o passing_sites.vcf.gz; bcftools index -f passing_sites.vcf.gz
echo "passing sites: $(bcftools view -H passing_sites.vcf.gz | wc -l)"
# SKILL.md genotype-level command, verbatim
bcftools filter -S . -e 'FMT/GQ<20 | FMT/DP<8' passing_sites.vcf.gz -Oz -o gt_filtered.vcf.gz; echo "genotype filter exit=$?"
bcftools index -f gt_filtered.vcf.gz
echo "sites retained by -S . (genotype-level, site kept): $(bcftools view -H gt_filtered.vcf.gz | wc -l)"
bcftools query -l cohort.vcf.gz | tr -d '\r' | tr '\n' ' '; echo
for f in passing_sites gt_filtered; do
  echo "[$f] per-sample ./. : $(bcftools query -f '[%GT\t]\n' $f.vcf.gz | tr -d '\r' | awk '{for(i=1;i<=NF;i++) if($i=="./.") m[i]++} END{for(i=1;i<=8;i++) printf m[i]+0" "}')"
done
echo "genotypes that are GQ<20 or DP<8 but not no-call before: $(bcftools query -i 'GT!="mis"' -f '[%GT:%GQ:%DP\t]\n' passing_sites.vcf.gz | tr -d '\r' | tr '\t' '\n' | awk -F: 'NF==3 && $1!="./." && ($2<20 || $3<8)' | wc -l)"
echo "== did -S . touch ONLY the failing genotypes? count of failing genotypes left un-nulled after: $(bcftools query -f '[%GT:%GQ:%DP\t]\n' gt_filtered.vcf.gz | tr -d '\r' | tr '\t' '\n' | awk -F: 'NF==3 && $1!="./." && ($2!="." && $2<20 || $3<8)' | wc -l)"
echo "== per-site missingness / HWE-type effect: sites with F_MISSING>=0.05 before vs after =="
echo "before: $(bcftools view -H -i 'F_MISSING>=0.05' passing_sites.vcf.gz | wc -l)  after: $(bcftools view -H -i 'F_MISSING>=0.05' gt_filtered.vcf.gz | wc -l)"
echo "== ExcessHet-style check with bcftools +fill-tags HWE before/after =="
for f in passing_sites gt_filtered; do
  bcftools +fill-tags $f.vcf.gz -- -t HWE,ExcHet 2>/dev/null | bcftools query -f '%HWE\n' | tr -d '\r' | awk -v n=$f '$1<0.001{c++} END{print n": sites HWE p<0.001 = "c+0}'
done
