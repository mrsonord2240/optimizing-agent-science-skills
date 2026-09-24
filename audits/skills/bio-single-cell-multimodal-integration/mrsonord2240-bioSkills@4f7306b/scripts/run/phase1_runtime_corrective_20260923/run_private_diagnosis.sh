#!/usr/bin/env bash
set -euo pipefail

private_lib=/home/sci/multimodal-private-20260923/packages
run_dir=/mnt/openscience/audits/bio-single-cell-multimodal-integration/run/phase1_runtime_corrective_20260923
source_root=/mnt/openscience/wt/single-cell-multimodal-integration/single-cell/multimodal-integration
fixture=/mnt/openscience/audits/bio-single-cell-multimodal-integration/run/phase2_20260923/input7_python_wnn/filtered_feature_bc_matrix.h5

PYTHONPATH="$private_lib" python3 "$run_dir/inspect_muon_umap.py" > "$run_dir/inspect_muon_umap.log" 2>&1
mkdir -p "$run_dir/exact_source_before_fix"
cp "$fixture" "$run_dir/exact_source_before_fix/filtered_feature_bc_matrix.h5"
cd "$run_dir/exact_source_before_fix"
set +e
PYTHONPATH="$private_lib" python3 "$source_root/examples/cite_seq_analysis.py" > source_before_fix.log 2>&1
status=$?
set -e
printf 'source_before_fix_exit=%d\n' "$status" > source_before_fix.status
test "$status" -ne 0
