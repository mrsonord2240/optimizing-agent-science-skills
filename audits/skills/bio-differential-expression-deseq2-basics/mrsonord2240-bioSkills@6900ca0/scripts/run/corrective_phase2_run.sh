#!/usr/bin/env bash
# Runs the corrective Phase 2 suite and every shipped R example under the isolated WSL environment.
# Usage from Windows: wsl.exe -d science -u sci -- bash -lc 'bash /mnt/openscience/audits/.../corrective_phase2_run.sh'
set -euo pipefail

run_dir=/mnt/openscience/audits/bio-differential-expression-deseq2-basics/run
skill_dir=/mnt/openscience/wt/differential-expression-deseq2-basics/differential-expression/deseq2-basics
mamba=/home/sci/.local/bin/micromamba
run_r() {
  local label="$1"
  local script="$2"
  local code=0
  if "$mamba" run -n deseq2-repair-20260923 Rscript "$script" > "$run_dir/${label}.log" 2>&1; then
    code=0
  else
    code=$?
  fi
  printf '%s exit=%s\n' "$label" "$code" | tee -a "$run_dir/corrective_phase2_exit_codes.txt"
  if [ "$code" -ne 0 ]; then
    return "$code"
  fi
}

: > "$run_dir/corrective_phase2_exit_codes.txt"
run_r corrective_phase2_suite "$run_dir/corrective_phase2_suite.R"
run_r shipped_basic_workflow "$skill_dir/examples/basic_workflow.R"
run_r shipped_batch_correction "$skill_dir/examples/batch_correction.R"
run_r shipped_multi_condition "$skill_dir/examples/multi_condition.R"
printf 'ALL RUNS EXITED 0\n' | tee -a "$run_dir/corrective_phase2_exit_codes.txt"
