#!/usr/bin/env bash
set -euo pipefail

py_lib=/home/sci/multimodal-private-20260923/packages
r_runtime=/home/sci/scatac-private-20260923/bin/Rscript
source_root=/mnt/openscience/wt/single-cell-multimodal-integration/single-cell/multimodal-integration
old_run=/mnt/openscience/audits/bio-single-cell-multimodal-integration/run/phase2_20260923
run_dir=/mnt/openscience/audits/bio-single-cell-multimodal-integration/run/phase2_reaudit_4f7306b_20260923

"$r_runtime" --vanilla "$run_dir/parse_r_sources.R" "$source_root/examples/cite_seq_analysis.R" "$source_root/scripts/seurat_bridge_integration.R" > "$run_dir/parse_r_sources.log" 2>&1
"$r_runtime" --vanilla "$source_root/scripts/seurat_bridge_integration.R" "$old_run/bridge_ref.rds" "$old_run/bridge_multi.rds" "$old_run/bridge_query.rds" "$run_dir/bridge_private_wsl.rds" 20 2 LogNormalize > "$run_dir/bridge_private_wsl.log" 2>&1
"$r_runtime" --vanilla "$run_dir/check_bridge_output.R" "$run_dir/bridge_private_wsl.rds" > "$run_dir/bridge_check.log" 2>&1
PYTHONPATH="$py_lib" python3 "$run_dir/check_mode_a.py" "$run_dir/mode_a_response.md" > "$run_dir/mode_a_check.log" 2>&1
PYTHONPATH="$py_lib" python3 "$run_dir/check_glue_boundary.py" > "$run_dir/glue_boundary.log" 2>&1
printf 'private_phase2_tail_clean_exit\n' > "$run_dir/tail_complete.log"
