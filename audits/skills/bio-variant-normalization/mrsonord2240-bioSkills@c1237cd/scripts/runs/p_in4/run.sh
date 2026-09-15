#!/bin/bash
# Input 4 (Variant B, post-fix regression 2026-09-15; WSL part rebuilt from the pre-fix output): "Cohort A was normalized with
# vt (decompose + decompose_blocksub + normalize), cohort B with bcftools norm -m- -f. Comparing them we get extra private
# variants. Reconcile the representation." WSL: vt, bcftools 1.21. The REF-mismatch record is excluded first (-c x).
set -uo pipefail
export PATH=/tmp/vaca/env/bin:$PATH
D=../../data; R=$D/ref.fa
bcftools --version | head -1; vt 2>&1 | grep -m1 -i version
bgzip -c $D/callerB.vcf > B.vcf.gz; bcftools index -f B.vcf.gz
bcftools norm -f $R -c x B.vcf.gz -Oz -o clean.vcf.gz 2>/dev/null; bcftools index -f clean.vcf.gz
echo "== cohort A: vt pipeline =="
vt decompose -s clean.vcf.gz -o d1.vcf 2>/dev/null; vt decompose_blocksub d1.vcf -o d2.vcf 2>/dev/null
vt normalize -r $R d2.vcf -o A.vt.vcf 2>&1 | grep -E "total no" ; bgzip -f A.vt.vcf; bcftools index -f A.vt.vcf.gz
echo "== cohort B: bcftools norm -m- -f (no --atomize) =="
bcftools norm -m- -f $R clean.vcf.gz -Oz -o B.bcf.vcf.gz; bcftools index -f B.bcf.vcf.gz
echo "records: vt=$(bcftools view -H A.vt.vcf.gz | wc -l) bcftools=$(bcftools view -H B.bcf.vcf.gz | wc -l)"
rm -rf c1; bcftools isec -p c1 A.vt.vcf.gz B.bcf.vcf.gz
echo "private to vt-cohort: $(grep -v '^#' c1/0000.vcf | cut -f2,4,5 | tr '\t\n' ' ;')"
echo "private to bcftools-cohort: $(grep -v '^#' c1/0001.vcf | cut -f2,4,5 | tr '\t\n' ' ;')"
echo "== reconcile with the post-fix SKILL.md pipeline on both (split -> atomize -> left-align) =="
for x in A.vt B.bcf; do
  bcftools norm -m- $x.vcf.gz | bcftools norm --atomize | bcftools norm -f $R -Oz -o $x.std.vcf.gz; bcftools index -f $x.std.vcf.gz
done
rm -rf c2; bcftools isec -p c2 A.vt.std.vcf.gz B.bcf.std.vcf.gz
echo "after standardizing: private vt=$(grep -vc '^#' c2/0000.vcf) private bcf=$(grep -vc '^#' c2/0001.vcf) shared=$(grep -vc '^#' c2/0002.vcf)"
