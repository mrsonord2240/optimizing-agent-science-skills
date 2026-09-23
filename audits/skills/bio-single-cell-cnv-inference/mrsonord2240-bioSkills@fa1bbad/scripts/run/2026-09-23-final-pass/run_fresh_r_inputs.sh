#!/usr/bin/env bash
# Purpose: execute all fresh R-backed Phase 2 inputs in the existing CNV runtime.
# Usage: bash run_fresh_r_inputs.sh
set -euo pipefail
root=/mnt/openscience/audits/bio-single-cell-cnv-inference/2026-09-23-final-pass/run
mamba=/home/sci/.local/bin/micromamba
for script in input1_infercnv_fresh.R input2_copykat_fresh.R input4_numbat_columns_fresh.R input8_scevan_shipped_fresh.R input9_copykat_selector_fresh.R; do
  echo "=== ${script} ==="
  "$mamba" run -n cnv-audit Rscript "$root/$script" 2>&1 | tee "$root/${script%.R}.log"
done
