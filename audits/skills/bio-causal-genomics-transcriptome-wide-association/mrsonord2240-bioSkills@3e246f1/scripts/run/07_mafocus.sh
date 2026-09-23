#!/usr/bin/env bash
# Fresh MA-FOCUS interface execution using relative paths, as required on Windows.
set -euo pipefail
AUDIT='F:/OpenScience/audits/bio-causal-genomics-transcriptome-wide-association'
VENV='F:/OpenScience/audit-scratch/twas-final-pass-20260923/focus-venv'
VPY="$VENV/Scripts/python.exe"
focus() { "$VPY" "$VENV/Scripts/focus" "$@"; }
export VPY VENV
export -f focus
cd "$AUDIT/data/focus_final"
focus finemap \
  'gwas.sumstats:gwas.sumstats:gwas.sumstats' \
  '1000G_EUR/all:1000G_EUR/all:1000G_EUR/all' \
  'focus_gtex_v8_whole_blood.db:focus_gtex_v8_whole_blood.db:focus_gtex_v8_whole_blood.db' \
  --p-threshold 5e-8 --tissue Whole_Blood --locations '38:EUR-EAS-AFR' --out finalpass_ma
test -s finalpass_ma.focus.tsv
awk -F'\t' 'NR==1 || $4 == "GENE1" || $4 == "NULL"' finalpass_ma.focus.tsv
