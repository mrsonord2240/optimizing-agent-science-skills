#!/bin/bash
# Execute Phase 2 regression scripts from the archived 2026-09-17 re-audit against commit e46d106.
set -euo pipefail
RSH=/f/OpenScience/audit-envs/mendelian-randomization-analyst/r.sh
AUDIT=/f/OpenScience/audits/bio-causal-genomics-mediation-analysis
cd "$AUDIT/run"
for input in input1_canonical_eqtl input2_cmaverse_4way input3_edge_smalln input4_mvmr_mediation input5_hima_highdim input8_meddml_doubleml input9_twostep_mr_mediation input10_bca_case_sensitivity input12_evalue_fixed; do
  echo "=== ${input} ==="
  "$RSH" "$AUDIT/run/${input}.R" 2>&1 | tee "$AUDIT/run/${input}_output.txt"
  echo "ASSERT PASS: ${input} exited 0"
done
