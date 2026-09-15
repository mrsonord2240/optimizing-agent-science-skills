#!/bin/bash
# Input 7 (NEW, re-audit 2026-09-15, Edge): "Two centres both used the label SYN_S1 for DIFFERENT people. Rename batch2's
# sample before merging so genotypes are not mixed, and confirm the merged file keeps both people." SYNTHETIC data.
set -uo pipefail
bgzip -c ../../data/cohort.vcf > joint.vcf.gz; bcftools index -f joint.vcf.gz
bcftools view -s SYN_S1,SYN_S2 joint.vcf.gz -Oz -o b1.vcf.gz; bcftools index -f b1.vcf.gz
printf 'SYN_S7\tSYN_S1\n' > clash.txt
bcftools view -s SYN_S7 joint.vcf.gz | bcftools reheader -s clash.txt | bgzip -c > b2.vcf.gz; bcftools index -f b2.vcf.gz
echo "== merge as is =="; bcftools merge b1.vcf.gz b2.vcf.gz -Oz -o m_bad.vcf.gz 2>&1 | tail -1
echo "== SKILL.md reheader block (verbatim, names substituted) =="
printf 'SYN_S1\tSYN_S1_centreB\n' > rename.txt
bcftools reheader -s rename.txt b2.vcf.gz -o renamed.vcf.gz; echo "reheader exit=$?"; bcftools index -f renamed.vcf.gz
bcftools merge b1.vcf.gz renamed.vcf.gz -Oz -o m.vcf.gz; bcftools index -f m.vcf.gz
echo "samples: $(bcftools query -l m.vcf.gz | tr -d '\r' | tr '\n' ' ')"
echo "centreB genotypes identical to original SYN_S7: $(bcftools query -s SYN_S1_centreB -f '[%GT]\n' m.vcf.gz | tr -d '\r' | grep -v '^\./\.$' | md5sum | cut -c1-8) vs $(bcftools query -s SYN_S7 -f '%CHROM:%POS[%GT]\n' joint.vcf.gz -i 'GT!="0/0" || GT="0/0"' >/dev/null; bcftools view -s SYN_S7 joint.vcf.gz | bcftools query -f '[%GT]\n' | tr -d '\r' | grep -v '^\./\.$' | md5sum | cut -c1-8)"
echo "== --force-samples alternative =="
bcftools merge --force-samples b1.vcf.gz b2.vcf.gz -Oz -o mf.vcf.gz 2>&1 | tail -1; echo "samples: $(bcftools query -l mf.vcf.gz | tr -d '\r' | tr '\n' ' ')"
