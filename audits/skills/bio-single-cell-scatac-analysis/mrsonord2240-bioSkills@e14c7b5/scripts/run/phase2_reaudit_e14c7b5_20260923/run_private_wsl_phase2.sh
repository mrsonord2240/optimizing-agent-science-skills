#!/usr/bin/env bash
set -euo pipefail

runtime=/home/sci/scatac-private-20260923/bin/Rscript
source_root=/mnt/openscience/wt/single-cell-scatac-analysis/single-cell/scatac-analysis
audit_root=/mnt/openscience/audits/bio-single-cell-scatac-analysis
run_dir="$audit_root/run/phase2_reaudit_e14c7b5_20260923"
data="$audit_root/data/obj_qc.rds"

"$runtime" --version > "$run_dir/00_runtime_version.log" 2>&1
"$runtime" -e 'suppressPackageStartupMessages({library(Signac);library(Seurat);library(chromVAR)}); cat(sprintf("runtime_clean_exit Signac=%s Seurat=%s chromVAR=%s\\n", packageVersion("Signac"), packageVersion("Seurat"), packageVersion("chromVAR")))' > "$run_dir/00_runtime_smoke.log" 2>&1
"$runtime" --vanilla "$run_dir/01_core_lsi.R" "$data" "$run_dir/core_lsi.rds" > "$run_dir/01_core_lsi.log" 2>&1
"$runtime" --vanilla "$run_dir/02_depth_component_policy.R" "$run_dir/core_lsi.rds" > "$run_dir/02_depth_component_policy.log" 2>&1
"$runtime" --vanilla "$run_dir/03_depth_aware_da.R" "$data" "$run_dir/depth_aware_da.csv" > "$run_dir/03_depth_aware_da.log" 2>&1
for run in 1 2; do
  prefix="$run_dir/chromvar_run${run}"
  "$runtime" --vanilla "$source_root/scripts/run_chromvar.R" "$data" "$prefix" 0 1 > "$run_dir/04_chromvar_run${run}.log" 2>&1
  test -s "${prefix}_obj.rds"
  test -s "${prefix}_diff_motifs.csv"
done
cmp "$run_dir/chromvar_run1_diff_motifs.csv" "$run_dir/chromvar_run2_diff_motifs.csv"
cmp "$run_dir/chromvar_run1_obj.rds" "$run_dir/chromvar_run2_obj.rds"
sha256sum "$run_dir"/chromvar_run*_obj.rds "$run_dir"/chromvar_run*_diff_motifs.csv > "$run_dir/04_chromvar_sha256.txt"
"$runtime" --vanilla "$run_dir/05_assert_chromvar.R" "$run_dir/chromvar_run1_obj.rds" "$run_dir/chromvar_run2_obj.rds" "$run_dir/chromvar_run1_diff_motifs.csv" "$run_dir/chromvar_run2_diff_motifs.csv" > "$run_dir/05_assert_chromvar.log" 2>&1
"$runtime" --vanilla "$run_dir/06_parse_shipped_r.R" "$source_root/scripts/run_chromvar.R" "$source_root/examples/signac_workflow.R" > "$run_dir/06_parse_shipped_r.log" 2>&1
"$runtime" --vanilla "$run_dir/07_mode_a_validate.R" "$run_dir/07_mode_a_outputs.md" > "$run_dir/07_mode_a_validate.log" 2>&1
python3 -c 'import py_compile, sys; py_compile.compile(sys.argv[1], cfile=sys.argv[2], doraise=True)' "$source_root/examples/scatac_workflow.py" "$run_dir/scatac_workflow.pyc"
printf 'python_parse_clean_exit file=examples/scatac_workflow.py\n' > "$run_dir/08_parse_shipped_python.log"
printf 'private_wsl_phase2_clean_exit\n' > "$run_dir/99_complete.log"
