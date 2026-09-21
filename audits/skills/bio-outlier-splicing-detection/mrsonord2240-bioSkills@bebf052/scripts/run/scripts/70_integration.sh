#!/bin/bash
# SKILL.md "Variant + Outlier Integration": block 06 (bcftools) verbatim, then block 07 (R) verbatim. usage: 70_integration.sh <vcf> <tag>
R=/mnt/openscience/audits/bio-outlier-splicing-detection/run
cd $R/in6; vcf=$1; tag=$2; rm -rf w_$tag; mkdir w_$tag; cd w_$tag
cp ../$vcf spliceai_annotated.vcf
cp $R/ex_drop/fraser_workdir/PATIENT_001_outliers.tsv fraser_results.tsv
export PATH=/mnt/openscience/audit-envs/alternative-splicing/tools/bin:$PATH
bash <(sed 's#^bcftools#micromamba run -n as-core bcftools#' $R/blocks/06_bash.sh)
echo "== spliceai_raw.tsv"; cut -c1-150 spliceai_raw.tsv
