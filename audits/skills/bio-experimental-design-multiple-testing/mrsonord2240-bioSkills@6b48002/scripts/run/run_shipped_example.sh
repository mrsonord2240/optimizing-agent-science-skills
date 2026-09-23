#!/usr/bin/env bash
# Phase 2 execution of the shipped multiple-testing example.
# Usage: bash run_shipped_example.sh <skill-dir> <r-wrapper> <output-dir>
set -euo pipefail
skill_dir="$1"
r_wrapper="$2"
out_dir="$3"
mkdir -p "$out_dir"
cd "$skill_dir"
# The example's IHW retry design can invoke up to three child R processes; the
# owned process group is bounded here so a documented solver hang is recorded
# rather than leaving an audit process running indefinitely.
timeout --signal=TERM --kill-after=10s 90s "$r_wrapper" examples/multiple_testing_correction.R \
  >"$out_dir/shipped_example_stdout.txt" 2>"$out_dir/shipped_example_stderr.txt"
