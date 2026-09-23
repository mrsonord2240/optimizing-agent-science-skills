#!/usr/bin/env bash
# Purpose: independently execute the Skill.md Foldseek easy-search command with the cached 1ATP database fixture.
set -euo pipefail

RUN=/mnt/openscience/audits/bio-remote-homology/run/phase2
WORK="$RUN/work/foldseek_direct"
OUT="$RUN/outputs/08_foldseek_direct_search.txt"
rm -rf "$WORK"
mkdir -p "$WORK/tmp"
foldseek easy-search "$RUN/data/1atp.pdb" "$RUN/data/foldseek_fixture/afdb_sp" "$WORK/results.m8" "$WORK/tmp" \
  --format-output query,target,fident,alnlen,evalue,bits,prob,qtmscore,ttmscore,lddt --threads 8 >"$OUT" 2>&1
awk -F '\t' '$7 >= 0.99 && $8 >= 0.99 && $9 >= 0.99 && $10 >= 0.99 {ok=1} END {exit !ok}' "$WORK/results.m8"
cat "$WORK/results.m8" >>"$OUT"
echo 'PASS: direct documented easy-search command produced probability, both TM-scores, and lDDT >= 0.99.' >>"$OUT"
