#!/usr/bin/env bash
set -euo pipefail

# Regression of the documented PoPS wrapper against PoPS's own non-degenerate
# genome-wide schizophrenia example; output is audit-owned.
AUDIT=/f/OpenScience/audits/bio-causal-genomics-effector-gene-prioritization
SKILL="$AUDIT/run/skill_copy"
POPS=/f/OpenScience/audit-envs/mendelian-randomization-analyst/tools/pops
PY=/f/OpenScience/audit-envs/mendelian-randomization-analyst/venv-pops/Scripts/python.exe
OUT="$AUDIT/run/outputs/input3_pops_real"

rm -rf "$OUT"
mkdir -p "$OUT"
export PYTHONDONTWRITEBYTECODE=1
"$PY" "$SKILL/examples/pops_run.py" \
  --pops_repo "$POPS" \
  --magma_prefix "$POPS/example/data/magma_scores/PASS_Schizophrenia" \
  --gene_annot_path "$POPS/example/data/utils/gene_annot_jun10.txt" \
  --feature_mat_prefix "$POPS/example/data/features_munged/pops_features" \
  --control_features_path "$POPS/example/data/utils/features_jul17_control.txt" \
  --num_feature_chunks 2 \
  --out_prefix "$OUT/pops_out" > "$OUT/input3_pops_real.log"

test -s "$OUT/pops_out.preds"
N=$(tail -n +2 "$OUT/pops_out.preds" | wc -l | tr -d ' ')
[ "$N" -gt 18000 ]
awk -F '\t' 'NR==2 {min=$2; max=$2} NR>1 {if ($2<min) min=$2; if ($2>max) max=$2} END {if (max<=min) exit 1; printf "score_range=%.6g..%.6g\\n", min, max}' "$OUT/pops_out.preds" \
  | tee "$OUT/input3_pops_assertions.log"
echo "ASSERTIONS PASS: $N genome-wide genes and a non-degenerate PoPS score range."
