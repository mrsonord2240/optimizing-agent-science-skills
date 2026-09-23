#!/usr/bin/env bash
# Purpose: run the shipped PSI-BLAST, jackhmmer, and MMseqs2 iterative-profile example against the cached Swiss-Prot sample.
set -euo pipefail

RUN=/mnt/openscience/audits/bio-remote-homology/run/phase2
WORK="$RUN/work/iterative_profile"
OUT="$RUN/outputs/04_iterative_profile_shipped_script.txt"
QUERY="$RUN/skill-copy/data/P17612.fasta"
TARGET=/mnt/openscience/audit-envs/database-access/public-data/local-blast/swissprot_sample.fasta
rm -rf "$WORK"
mkdir -p "$WORK"
(
  cd "$WORK"
  bash "$RUN/skill-copy/iterative_profile.sh" "$QUERY" "$TARGET"
) >"$OUT" 2>&1
grep -q 'Q197B6' "$WORK/psiblast.tsv"
grep -q 'Q197B6' "$WORK/jackhmmer.tbl"
grep -q 'Q197B6' "$WORK/mmseqs.m8"
grep -q 'psiblast:' "$OUT"
grep -q 'jackhmmer:' "$OUT"
grep -q 'mmseqs2' "$OUT"
echo 'PASS: all three iterative methods recovered Q197B6 and the script printed its comparison summary.' >>"$OUT"
