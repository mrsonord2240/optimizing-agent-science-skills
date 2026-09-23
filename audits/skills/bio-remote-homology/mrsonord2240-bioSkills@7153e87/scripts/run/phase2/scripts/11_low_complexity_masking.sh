#!/usr/bin/env bash
# Purpose: test whether the Skill.md low-complexity mitigation actually emits a masked FASTA from its documented segmasker invocation.
set -euo pipefail

RUN=/mnt/openscience/audits/bio-remote-homology/run/phase2
OUT="$RUN/outputs/11_low_complexity_masking.txt"
WORK="$RUN/work/low_complexity_masking"
rm -rf "$WORK"
mkdir -p "$WORK"
segmasker -infmt fasta -in "$RUN/data/low_complexity.fa" >"$WORK/documented_output.txt"
segmasker -infmt fasta -in "$RUN/data/low_complexity.fa" -outfmt fasta >"$WORK/masked.fa"
segmasker -help >"$WORK/segmasker_help.txt"
grep -q '12 - 127' "$WORK/documented_output.txt"
grep -v '^>' "$WORK/masked.fa" | grep -q '[a-z]'
grep -q -- '-outfmt' "$WORK/segmasker_help.txt"
{
  echo 'Documented command output:'
  cat "$WORK/documented_output.txt"
  echo 'Explicit FASTA output:'
  cat "$WORK/masked.fa"
  echo 'Relevant help:'
  grep -A3 -B2 -i outfmt "$WORK/segmasker_help.txt"
  echo 'OBSERVED: the documented command reports intervals only; it does not itself emit a masked FASTA for the next profile command.'
} >"$OUT"
