#!/bin/bash
# Input 2: "ClinVar says our homopolymer deletion is absent" -- demonstrate the silent miss, then fix.
# Note: annotate is run on indexed files (mingw bcftools 1.24 refuses an unindexed stdin target when -a is a VCF).
set -uo pipefail
DATA=../../data
bgzip -c $DATA/callerB.vcf > callerB.vcf.gz && bcftools index -f callerB.vcf.gz
for db in clinvar_syn dbsnp_syn; do bgzip -c $DATA/$db.vcf > $db.vcf.gz; bcftools index -f $db.vcf.gz; done
ann() { bcftools annotate -a clinvar_syn.vcf.gz -c INFO/CLNSIG,INFO/CLNREVSTAT "$1" -Oz -o tmp1.vcf.gz && bcftools index -f tmp1.vcf.gz && \
        bcftools annotate -a dbsnp_syn.vcf.gz -c ID tmp1.vcf.gz | bcftools query -f '%CHROM:%POS %REF>%ALT\t%ID\t%INFO/CLNSIG\t%INFO/CLNREVSTAT\n'; }
echo "== RAW callerB annotated against ClinVar/dbSNP =="; ann callerB.vcf.gz
echo "== normalized (split -> atomize -> left-align vs the SAME ref, REF mismatch excluded) =="
bcftools norm -m- callerB.vcf.gz 2>/dev/null | bcftools norm --atomize 2>/dev/null | \
  bcftools norm -f $DATA/ref.fa -c x -Oz -o for_annotation.vcf.gz 2> norm.log; bcftools index -f for_annotation.vcf.gz; cat norm.log
ann for_annotation.vcf.gz
echo "== Skill order as written (atomize first), site chr1:2000 only =="
bcftools norm --atomize callerB.vcf.gz 2>/dev/null | bcftools norm -m- 2>/dev/null | bcftools norm -f $DATA/ref.fa -c x -Oz -o skillorder.vcf.gz 2>/dev/null; bcftools index -f skillorder.vcf.gz
ann skillorder.vcf.gz | awk '$1 ~ /:2000$/'
