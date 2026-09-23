#!/usr/bin/env bash
set -euo pipefail

runtime=/home/sci/scatac-private-20260923/bin/Rscript
source_root=/mnt/openscience/wt/single-cell-scatac-analysis/single-cell/scatac-analysis
audit_root=/mnt/openscience/audits/bio-single-cell-scatac-analysis
out_dir="$audit_root/run/phase1_runtime_corrective_20260923/private_wsl_exact"
mkdir -p "$out_dir"

for run in 1 2; do
  prefix="$out_dir/chromvar_run${run}"
  "$runtime" "$source_root/scripts/run_chromvar.R" "$audit_root/data/obj_qc.rds" "$prefix" 0 1 \
    >"$out_dir/chromvar_run${run}.console.txt" 2>&1
  test -s "${prefix}_obj.rds"
  test -s "${prefix}_diff_motifs.csv"
done

cmp "$out_dir/chromvar_run1_diff_motifs.csv" "$out_dir/chromvar_run2_diff_motifs.csv"
sha256sum "$out_dir"/chromvar_run*_obj.rds "$out_dir"/chromvar_run*_diff_motifs.csv > "$out_dir/artifact_sha256.txt"
