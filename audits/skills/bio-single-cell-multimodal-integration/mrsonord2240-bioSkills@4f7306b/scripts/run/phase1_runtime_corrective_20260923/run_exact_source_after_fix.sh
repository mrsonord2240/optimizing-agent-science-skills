#!/usr/bin/env bash
set -euo pipefail

private_lib=/home/sci/multimodal-private-20260923/packages
run_dir=/mnt/openscience/audits/bio-single-cell-multimodal-integration/run/phase1_runtime_corrective_20260923
source_root=/mnt/openscience/wt/single-cell-multimodal-integration/single-cell/multimodal-integration
fixture=/mnt/openscience/audits/bio-single-cell-multimodal-integration/run/phase2_20260923/input7_python_wnn/filtered_feature_bc_matrix.h5

mkdir -p "$run_dir/exact_source_after_fix"
cp "$fixture" "$run_dir/exact_source_after_fix/filtered_feature_bc_matrix.h5"
cd "$run_dir/exact_source_after_fix"
PYTHONPATH="$private_lib" python3 "$source_root/examples/cite_seq_analysis.py" > source_after_fix.log 2>&1
test -s cite_seq_analyzed.h5mu
test -s umap_cite_seq_wnn.pdf
PYTHONPATH="$private_lib" python3 "$run_dir/check_exact_source_output.py" cite_seq_analyzed.h5mu > check_output.log 2>&1
printf 'exact_source_after_fix_clean_exit\n' > complete.log
