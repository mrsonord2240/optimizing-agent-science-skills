#!/usr/bin/env bash
# Purpose: execute the shipped Foldseek structure-query script with a cached 1ATP database fixture, avoiding multi-GB AFDB download.
set -euo pipefail

RUN=/mnt/openscience/audits/bio-remote-homology/run/phase2
WORK="$RUN/work/foldseek_shipped_script"
OUT="$RUN/outputs/03_foldseek_shipped_script.txt"
rm -rf "$WORK"
mkdir -p "$WORK/tmp"
(
  cd "$WORK"
  bash "$RUN/skill-copy/foldseek_search.sh" "$RUN/data/1atp.pdb" "$RUN/data/foldseek_fixture" "$WORK/tmp"
) >"$OUT" 2>&1
awk -F '\t' '$7 >= 0.99 && $8 >= 0.99 && $9 >= 0.99 && $10 >= 0.99 {ok=1} END {exit !ok}' "$WORK/results.m8"
cat "$WORK/results.m8" >>"$OUT"
echo 'PASS: shipped structure branch reused .dbtype cache and produced a high-confidence 1ATP self-hit.' >>"$OUT"
