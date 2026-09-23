#!/usr/bin/env bash
# Repeats the exact shipped-example runner to measure the documented IHW crash behavior.
# Usage: bash repeat_shipped_example.sh <runner> <skill-dir> <r-wrapper> <output-root>
set -u
runner="$1"
skill_dir="$2"
r_wrapper="$3"
out_root="$4"
mkdir -p "$out_root"
for i in 1 2 3; do
  out="$out_root/repeat_$i"
  mkdir -p "$out"
  "$runner" "$skill_dir" "$r_wrapper" "$out"
  status=$?
  printf 'run=%s exit=%s\n' "$i" "$status" >> "$out_root/repeat_status.txt"
done
