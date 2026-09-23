#!/usr/bin/env bash
# Purpose: print the assertion-bearing last line from each fresh runtime log.
# Usage: bash summarize_fresh_logs.sh
set -euo pipefail
root=/mnt/openscience/audits/bio-single-cell-cnv-inference/2026-09-23-final-pass/run
for stem in input1_infercnv_fresh input2_copykat_fresh input4_numbat_columns_fresh input8_scevan_shipped_fresh input9_copykat_selector_fresh; do
  printf '%s: ' "$stem"
  tail -n 1 "$root/$stem.log"
done
