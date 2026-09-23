#!/usr/bin/env bash
# Fresh two-tissue execution of the shipped S-PrediXcan/S-MultiXcan workflow.
set -euo pipefail
AUDIT='F:/OpenScience/audits/bio-causal-genomics-transcriptome-wide-association'
PY='F:/OpenScience/audit-envs/mendelian-randomization-analyst/metaxcan-venv/Scripts/python.exe'
MX='F:/OpenScience/audit-envs/mendelian-randomization-analyst/tools/MetaXcan/software'
DATA="$AUDIT/data/smultixcan"
GWAS="$AUDIT/data/spredixcan/gwas.sumstats.p.txt"
OUT="$DATA/finalpass_out"
mkdir -p "$OUT"
for tissue in Tissue1 Tissue2; do
  "$PY" "$MX/SPrediXcan.py" --model_db_path "$DATA/models/$tissue.db" \
    --covariance "$DATA/snp_covariance.txt" --gwas_file "$GWAS" --snp_column SNP \
    --effect_allele_column A1 --non_effect_allele_column A2 --beta_column BETA \
    --pvalue_column P --output_file "$OUT/$tissue.csv"
done
"$PY" "$MX/SMulTiXcan.py" --models_folder "$DATA/models" --models_name_pattern '(.*)\.db' \
  --snp_covariance "$DATA/snp_covariance.txt" --metaxcan_folder "$OUT" \
  --metaxcan_filter '(.*)\.csv' --metaxcan_file_name_parse_pattern '(.*)\.csv' \
  --gwas_file "$GWAS" --snp_column SNP --effect_allele_column A1 \
  --non_effect_allele_column A2 --beta_column BETA --pvalue_column P \
  --regularization 0.1 --cutoff_condition_number 30 --throw \
  --output "$DATA/finalpass_joint.csv"
test -s "$DATA/finalpass_joint.csv"
awk -F'\t' 'NR==1 || $1 == "GENE1" || $1 == "GENE2"' "$DATA/finalpass_joint.csv"
awk -F'\t' 'NR==1 {for(i=1;i<=NF;i++)if($i=="pvalue")p=i; print; next} p && $p < 2.3e-6 {print}' \
  "$DATA/finalpass_joint.csv" > "$DATA/finalpass_joint_sig.csv"
cat "$DATA/finalpass_joint_sig.csv"
