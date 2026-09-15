#!/bin/bash
# Input 4: cohort A normalized with vt (decompose + decompose_blocksub + normalize), cohort B with bcftools norm -m- -f (no --atomize).
# Show the representation discordance the Skill predicts, then reconcile by standardizing on bcftools with --atomize.
set -u
R=../../data/ref.fa
bgzip -c ../../data/callerB.vcf | bcftools view -e 'POS==4000' -Oz -o B.vcf.gz; bcftools index -f B.vcf.gz   # drop the REF-mismatch site for this test
echo "== cohort A: vt pipeline =="
vt decompose -s B.vcf.gz -o - 2>/dev/null | vt decompose_blocksub - -o - 2>/dev/null | vt normalize -r $R - -o cohortA_vt.vcf 2>&1 | grep -iE 'total|normalized' | head -4
echo "== cohort B: bcftools norm -m- -f (no --atomize) =="
bcftools norm -m- -f $R B.vcf.gz -Oz -o cohortB_bcf.vcf.gz 2>&1 | tail -1
bgzip -f cohortA_vt.vcf; bcftools index -f cohortA_vt.vcf.gz; bcftools index -f cohortB_bcf.vcf.gz
echo "records: vt=$(bcftools view -H cohortA_vt.vcf.gz | wc -l) bcftools=$(bcftools view -H cohortB_bcf.vcf.gz | wc -l)"
rm -rf disc; bcftools isec -p disc cohortA_vt.vcf.gz cohortB_bcf.vcf.gz
echo "private to vt-cohort:"; grep -v '^#' disc/0000.vcf | cut -f1-5
echo "private to bcftools-cohort:"; grep -v '^#' disc/0001.vcf | cut -f1-5
echo "== reconcile: bcftools split -> atomize -> left-align, same flags on both =="
bcftools norm -m- B.vcf.gz 2>/dev/null | bcftools norm --atomize 2>/dev/null | bcftools norm -f $R -Oz -o cohortB_std.vcf.gz 2>/dev/null; bcftools index -f cohortB_std.vcf.gz
rm -rf rec; bcftools isec -p rec cohortA_vt.vcf.gz cohortB_std.vcf.gz
echo "after standardizing: private vt=$(grep -vc '^#' rec/0000.vcf) private bcf=$(grep -vc '^#' rec/0001.vcf) shared=$(grep -vc '^#' rec/0002.vcf)"
