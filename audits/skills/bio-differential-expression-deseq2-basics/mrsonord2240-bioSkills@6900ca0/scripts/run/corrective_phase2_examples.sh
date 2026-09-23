#!/usr/bin/env bash
# Re-runs all three shipped R examples after the corrective regression suite.
# It is intentionally separate so each source example has an independently recorded clean exit.
set -euo pipefail

run_dir=/mnt/openscience/audits/bio-differential-expression-deseq2-basics/run
skill_dir=/mnt/openscience/wt/differential-expression-deseq2-basics/differential-expression/deseq2-basics
mamba=/home/sci/.local/bin/micromamba
: > "$run_dir/corrective_phase2_examples_exit_codes.txt"
for example in basic_workflow batch_correction multi_condition; do
  "$mamba" run -n deseq2-repair-20260923 Rscript "$skill_dir/examples/${example}.R" \
    > "$run_dir/shipped_${example}.log" 2>&1
  printf '%s exit=0\n' "$example" | tee -a "$run_dir/corrective_phase2_examples_exit_codes.txt"
done
printf 'ALL SHIPPED EXAMPLES EXITED 0\n' | tee -a "$run_dir/corrective_phase2_examples_exit_codes.txt"
