#!/usr/bin/env bash
# Run the exact shipped example from the audited tip with its shipped safe helpers.
# Usage: bash run_exact_shipped_example.sh <skill-dir> <r-wrapper> <output-dir>
set -euo pipefail
skill_dir="$1"
r_wrapper="$2"
out_dir="$3"
mkdir -p "$out_dir"
cd "$skill_dir"
timeout --signal=TERM --kill-after=10s 120s "$r_wrapper" examples/multiple_testing_correction.R \
  >"$out_dir/shipped_example_stdout.txt" 2>"$out_dir/shipped_example_stderr.txt"
grep -q '^q-value: pi0 = ' "$out_dir/shipped_example_stdout.txt"
grep -Eq '^IHW (discoveries at FDR|did not complete after)' "$out_dir/shipped_example_stdout.txt"
grep -q ' BH ' "$out_dir/shipped_example_stdout.txt"
