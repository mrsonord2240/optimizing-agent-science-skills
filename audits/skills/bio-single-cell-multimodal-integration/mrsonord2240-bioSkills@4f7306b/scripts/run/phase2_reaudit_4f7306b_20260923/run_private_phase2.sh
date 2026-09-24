#!/usr/bin/env bash
set -euo pipefail

py_lib=/home/sci/multimodal-private-20260923/packages
r_runtime=/home/sci/scatac-private-20260923/bin/Rscript
source_root=/mnt/openscience/wt/single-cell-multimodal-integration/single-cell/multimodal-integration
old_run=/mnt/openscience/audits/bio-single-cell-multimodal-integration/run/phase2_20260923
run_dir=/mnt/openscience/audits/bio-single-cell-multimodal-integration/run/phase2_reaudit_4f7306b_20260923

PYTHONPATH="$py_lib" python3 -c 'import py_compile,sys; py_compile.compile(sys.argv[1], cfile=sys.argv[2], doraise=True)' "$source_root/examples/cite_seq_analysis.py" "$run_dir/cite_seq_analysis.pyc"
mkdir -p "$run_dir/python_wnn"
cp "$old_run/input7_python_wnn/filtered_feature_bc_matrix.h5" "$run_dir/python_wnn/filtered_feature_bc_matrix.h5"
cd "$run_dir/python_wnn"
PYTHONPATH="$py_lib" python3 "$source_root/examples/cite_seq_analysis.py" > source.log 2>&1
test -s cite_seq_analyzed.h5mu
test -s umap_cite_seq_wnn.pdf
PYTHONPATH="$py_lib" python3 "$run_dir/check_python_wnn.py" cite_seq_analyzed.h5mu > check.log 2>&1

"$r_runtime" --vanilla "$run_dir/parse_r_sources.R" "$source_root/examples/cite_seq_analysis.R" "$source_root/scripts/seurat_bridge_integration.R" > parse_r_sources.log 2>&1
"$r_runtime" --vanilla "$source_root/scripts/seurat_bridge_integration.R" "$old_run/bridge_ref.rds" "$old_run/bridge_multi.rds" "$old_run/bridge_query.rds" "$run_dir/bridge_private_wsl.rds" 20 2 LogNormalize > bridge_private_wsl.log 2>&1
"$r_runtime" --vanilla "$run_dir/check_bridge_output.R" "$run_dir/bridge_private_wsl.rds" > bridge_check.log 2>&1

PYTHONPATH="$py_lib" python3 "$run_dir/check_mode_a.py" "$run_dir/mode_a_response.md" > mode_a_check.log 2>&1
PYTHONPATH="$py_lib" python3 "$run_dir/check_glue_boundary.py" > glue_boundary.log 2>&1
printf 'private_phase2_clean_exit\n' > complete.log
