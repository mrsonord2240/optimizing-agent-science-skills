#!/bin/bash
# WSL part of input 2: vcftools --relatedness2 (KING-robust), somalier extract/relate, peddy (if installable).
set -uo pipefail
cd "$(dirname "$0")"
export PATH=/tmp/vaca/env/bin:$PATH
S=../../data
vcftools --version
echo "== SKILL.md: vcftools --gzvcf input.vcf.gz --relatedness2 --out kin =="
vcftools --gzvcf cohort.vcf.gz --relatedness2 --out kin > kin.log 2>&1; echo "exit=$?"
awk 'NR==1 || ($1!=$2)' kin.relatedness2 | sort -k7,7gr | head -6
echo "KING bands (SKILL.md): >0.354 dup/MZ, 0.177-0.354 1st, 0.0884-0.177 2nd"
Q=/tmp/vaca/qc/bin
if [ -x $Q/somalier ]; then
  echo "== somalier $($Q/somalier 2>&1 | grep -m1 -i version) =="
  bcftools view -G cohort.vcf.gz -Oz -o sites.vcf.gz; bcftools index -t -f sites.vcf.gz
  rm -rf extracted; mkdir -p extracted
  $Q/somalier extract -d extracted/ --sites sites.vcf.gz -f $S/ref.fa cohort.vcf.gz > som_extract.log 2>&1; echo "extract exit=$?"; tail -2 som_extract.log
  awk 'BEGIN{OFS="\t"} {print $1,$2,$3,$4,$5,$6}' $S/cohort.ped > cohort.ped
  $Q/somalier relate --ped cohort.ped extracted/*.somalier > som_relate.log 2>&1; echo "relate exit=$?"; tail -2 som_relate.log
  [ -f somalier.pairs.tsv ] && sort -t$'\t' -k3,3gr somalier.pairs.tsv | cut -f1-6 | head -4
else
  echo "somalier not installed: $(tail -3 /tmp/vaca/qc_install.log)"
fi
if [ -x $Q/python ] && $Q/python -c "import peddy" 2>/dev/null; then
  echo "== peddy (SKILL.md: python -m peddy -p 4 --plot --prefix cohort_qc input.vcf.gz cohort.ped) =="
  $Q/python -m peddy -p 4 --plot --prefix cohort_qc cohort.vcf.gz cohort.ped > peddy.log 2>&1; echo "peddy exit=$?"; tail -4 peddy.log
fi
