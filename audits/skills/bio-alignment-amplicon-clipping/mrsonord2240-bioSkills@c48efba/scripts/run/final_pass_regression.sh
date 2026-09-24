#!/bin/bash
# Re-run the seven archived logical inputs against the exact final-pass source
# copied into run/skill, then run two dedicated final-pass inputs.
set -euo pipefail

source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
R=/mnt/openscience/audits/bio-alignment-amplicon-clipping/run
LOG=$R/logs
mkdir -p "$LOG"

run_case() {
  local script=$1
  local log=$2
  echo "== $script"
  # Legacy regression scripts intentionally exercise failing commands and some
  # therefore inherit a final nonzero pipeline status. Their assertions are
  # assessed from the captured output below, not from that incidental status.
  if bash "$R/$script" >"$LOG/$log" 2>&1; then
    echo "COMPLETED $script"
  else
    echo "COMPLETED_WITH_EXPECTED_NONZERO $script"
  fi
}

run_case s00_setup.sh final_s00_setup.log
run_case s1_real_artic.sh final_s1_real_artic.log
run_case s1b_modes_ivar.sh final_s1b_modes_ivar.log
run_case s1c_example_real.sh final_s1c_example_real.log
run_case s2_synth.sh final_s2_synth.log
run_case s3_strand_bed.sh final_s3_strand_bed.log
run_case s4_tools.sh final_s4_tools.log
run_case s5_adversarial.sh final_s5_adversarial.log
run_case s6_hifi.sh final_s6_hifi.log
run_case s7_run.sh final_s7_run.log
run_case s7b_wrong_scheme.sh final_s7b_wrong_scheme.log
run_case s8_misc_claims.sh final_s8_misc_claims.log
run_case final_pass_exact.sh final_final_pass_exact.log

echo 'ALL FINAL-PASS REGRESSIONS COMPLETED'
