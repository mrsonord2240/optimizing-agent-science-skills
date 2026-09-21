#!/bin/bash
# Input 4: SpliceAI + Pangolin on malformed/edge records (GRCh37 chrX), commands from SKILL.md; then the Skill's unscored_report / parsers on the output.
export PYTHONDONTWRITEBYTECODE=1
AS=/mnt/openscience/audit-envs/alternative-splicing
FA=$AS/public-data/derived/X.fa; DB=$AS/public-data/derived/chrX_GRCh37_ensembl.gffutils.db
cd /mnt/openscience/audits/bio-splice-variant-prediction/run
for n in edge_grch37 edge_chr_prefixed edge_star_allele edge_symbolic_DEL aso_mask; do
  micromamba run -n as-spliceai spliceai -I data/$n.vcf -O out/sai_$n.vcf -R $FA -A grch37 -D 50 -M 0 > out/sai_$n.log 2>&1
  echo "SpliceAI $n rc=$? in=$(grep -vc '^#' data/$n.vcf) out=$(grep -vc '^#' out/sai_$n.vcf 2>/dev/null) tagged=$(grep -c 'SpliceAI=' out/sai_$n.vcf 2>/dev/null)"
done
for n in edge_grch37 edge_chr_prefixed edge_star_allele; do
  micromamba run -n as-pangolin pangolin data/$n.vcf $FA $DB out/pang_$n -d 50 -m False > out/pang_$n.log 2>&1
  echo "Pangolin $n rc=$? in=$(grep -vc '^#' data/$n.vcf) out=$(grep -vc '^#' out/pang_$n.vcf 2>/dev/null) tagged=$(grep -c 'Pangolin=' out/pang_$n.vcf 2>/dev/null)"
done
