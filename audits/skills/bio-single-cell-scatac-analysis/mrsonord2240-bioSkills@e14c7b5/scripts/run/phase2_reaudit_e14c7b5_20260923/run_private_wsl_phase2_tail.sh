#!/usr/bin/env bash
set -euo pipefail
runtime=/home/sci/scatac-private-20260923/bin/Rscript
source_root=/mnt/openscience/wt/single-cell-scatac-analysis/single-cell/scatac-analysis
run_dir=/mnt/openscience/audits/bio-single-cell-scatac-analysis/run/phase2_reaudit_e14c7b5_20260923
"$runtime" --vanilla "$run_dir/05_assert_chromvar.R" "$run_dir/chromvar_run1_obj.rds" "$run_dir/chromvar_run2_obj.rds" "$run_dir/chromvar_run1_diff_motifs.csv" "$run_dir/chromvar_run2_diff_motifs.csv" > "$run_dir/05_assert_chromvar.log" 2>&1
"$runtime" --vanilla "$run_dir/06_parse_shipped_r.R" "$source_root/scripts/run_chromvar.R" "$source_root/examples/signac_workflow.R" > "$run_dir/06_parse_shipped_r.log" 2>&1
"$runtime" --vanilla "$run_dir/07_mode_a_validate.R" "$run_dir/07_mode_a_outputs.md" > "$run_dir/07_mode_a_validate.log" 2>&1
python3 -c 'import py_compile, sys; py_compile.compile(sys.argv[1], cfile=sys.argv[2], doraise=True)' "$source_root/examples/scatac_workflow.py" "$run_dir/scatac_workflow.pyc"
printf 'python_parse_clean_exit file=examples/scatac_workflow.py\n' > "$run_dir/08_parse_shipped_python.log"
printf 'private_wsl_phase2_clean_exit\n' > "$run_dir/99_complete.log"
