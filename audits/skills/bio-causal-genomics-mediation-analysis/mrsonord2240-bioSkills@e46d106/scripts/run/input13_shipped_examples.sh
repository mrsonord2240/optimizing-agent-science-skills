#!/bin/bash
# Phase 2 regression: run every executable in the Skill's shipped examples directory.
set -euo pipefail
RSH=/f/OpenScience/audit-envs/mendelian-randomization-analyst/r.sh
SKILL=/f/OpenScience/wt/causal-genomics-mediation-analysis/causal-genomics/mediation-analysis
for example in eqtl_mediation.R sensitivity_analysis.R cmaverse_4way.R mvmr_mediation.R; do
  echo "=== ${example} ==="
  "$RSH" "$SKILL/examples/$example"
  echo "ASSERT PASS: ${example} exited 0"
done
