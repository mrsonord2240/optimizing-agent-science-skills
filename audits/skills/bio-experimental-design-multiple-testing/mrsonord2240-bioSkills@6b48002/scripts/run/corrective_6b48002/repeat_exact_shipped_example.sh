#!/usr/bin/env bash
# Repeatedly run the exact full shipped example; any nonzero exit fails this audit.
# Usage: bash repeat_exact_shipped_example.sh <runner> <skill-dir> <r-wrapper> <output-root>
set -euo pipefail
runner="$1"
skill_dir="$2"
r_wrapper="$3"
out_root="$4"
mkdir -p "$out_root"
: >"$out_root/repeat_status.txt"
for i in 1 2 3; do
  out="$out_root/repeat_$i"
  "$runner" "$skill_dir" "$r_wrapper" "$out"
  printf 'run=%s exit=0\n' "$i" >>"$out_root/repeat_status.txt"
done
