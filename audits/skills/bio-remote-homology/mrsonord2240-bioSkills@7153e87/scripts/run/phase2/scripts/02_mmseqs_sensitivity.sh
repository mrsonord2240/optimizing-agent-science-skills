#!/usr/bin/env bash
# Purpose: regression-test the documented MMseqs2 default-vs--s 7.5 remote-homology sensitivity claim.
set -euo pipefail

RUN=/mnt/openscience/audits/bio-remote-homology/run/phase2
WORK="$RUN/work/mmseqs_sensitivity"
OUT="$RUN/outputs/02_mmseqs_sensitivity.txt"
QUERY="$RUN/skill-copy/data/P17612.fasta"
TARGET=/mnt/openscience/audit-envs/database-access/public-data/local-blast/swissprot_sample.fasta
rm -rf "$WORK"
mkdir -p "$WORK"
mmseqs easy-search "$QUERY" "$TARGET" "$WORK/default.m8" "$WORK/tmp_default" -e 1e-5 \
  --format-output query,target,fident,evalue,bits >"$OUT" 2>&1
mmseqs easy-search "$QUERY" "$TARGET" "$WORK/s75.m8" "$WORK/tmp_s75" -s 7.5 -e 1e-5 \
  --format-output query,target,fident,evalue,bits >>"$OUT" 2>&1
test ! -s "$WORK/default.m8"
grep -q 'Q197B6' "$WORK/s75.m8"
printf 'default_lines=%s\ns75_result=\n' "$(wc -l < "$WORK/default.m8")" >>"$OUT"
cat "$WORK/s75.m8" >>"$OUT"
echo 'PASS: default search had zero rows and -s 7.5 recovered Q197B6.' >>"$OUT"
