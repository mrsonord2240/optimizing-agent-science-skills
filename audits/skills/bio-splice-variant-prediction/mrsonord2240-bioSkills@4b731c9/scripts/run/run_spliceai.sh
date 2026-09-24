#!/bin/bash
# Input 1/4: SpliceAI exactly as SKILL.md "SpliceAI Workflow" (spliceai -I -O -R -A -D -M); GRCh37 because X.fa is GRCh37.
export PYTHONDONTWRITEBYTECODE=1
R=/mnt/openscience/audits/bio-splice-variant-prediction/run
FA=/mnt/openscience/audit-envs/alternative-splicing/public-data/derived/X.fa
cd $R
for cfg in "50 0" "500 0" "2000 0"; do
  set -- $cfg
  /mnt/openscience/audit-envs/alternative-splicing/tools/bin/spliceai -I data/panel_grch37.vcf -O out/sai_D$1_M$2.vcf -R $FA -A grch37 -D $1 -M $2 > out/sai_D$1_M$2.log 2>&1
  echo "D=$1 M=$2 rc=$? records_out=$(grep -vc '^#' out/sai_D$1_M$2.vcf) with_SpliceAI=$(grep -c 'SpliceAI=' out/sai_D$1_M$2.vcf)"
done
