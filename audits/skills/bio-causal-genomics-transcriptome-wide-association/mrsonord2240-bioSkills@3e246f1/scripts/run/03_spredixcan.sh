#!/usr/bin/env bash
# Fresh canonical S-PrediXcan execution with the exact explicit GWAS-column flags.
set -euo pipefail
AUDIT='F:/OpenScience/audits/bio-causal-genomics-transcriptome-wide-association'
PY='F:/OpenScience/audit-envs/mendelian-randomization-analyst/metaxcan-venv/Scripts/python.exe'
SP='F:/OpenScience/audit-envs/mendelian-randomization-analyst/tools/MetaXcan/software/SPrediXcan.py'
DATA="$AUDIT/data/spredixcan"
"$PY" "$SP" \
  --model_db_path "$DATA/synthetic_model.db" --covariance "$DATA/synthetic.cov.txt" \
  --gwas_file "$DATA/gwas.sumstats.p.txt" --snp_column SNP \
  --effect_allele_column A1 --non_effect_allele_column A2 \
  --beta_column BETA --pvalue_column P --output_file "$DATA/finalpass_spredixcan.csv"
test -s "$DATA/finalpass_spredixcan.csv"
cat "$DATA/finalpass_spredixcan.csv"
