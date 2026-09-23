#!/usr/bin/env bash
# Purpose: regression-test DIAMOND mode selection and jackhmmer cross-validation on the real twilight-zone kinase pair.
set -euo pipefail

RUN=/mnt/openscience/audits/bio-remote-homology/run/phase2
WORK="$RUN/work/diamond_jackhmmer"
OUT="$RUN/outputs/05_diamond_jackhmmer.txt"
QUERY="$RUN/skill-copy/data/P17612.fasta"
TARGET=/mnt/openscience/audit-envs/database-access/public-data/local-blast/swissprot_sample.fasta
rm -rf "$WORK"
mkdir -p "$WORK"
diamond makedb --in "$TARGET" -d "$WORK/swissprot" >"$OUT" 2>&1
diamond blastp -d "$WORK/swissprot" -q "$QUERY" -o "$WORK/default.tsv" -e 1 --outfmt 6 qseqid sseqid pident evalue bitscore >>"$OUT" 2>&1
diamond blastp -d "$WORK/swissprot" -q "$QUERY" -o "$WORK/more.tsv" --more-sensitive -e 1 --outfmt 6 qseqid sseqid pident evalue bitscore >>"$OUT" 2>&1
diamond blastp -d "$WORK/swissprot" -q "$QUERY" -o "$WORK/ultra.tsv" --ultra-sensitive -e 1 --outfmt 6 qseqid sseqid pident evalue bitscore >>"$OUT" 2>&1
jackhmmer -N 3 --tblout "$WORK/jackhmmer.tbl" "$QUERY" "$TARGET" >>"$OUT" 2>&1
test ! -s "$WORK/default.tsv"
test ! -s "$WORK/more.tsv"
grep -q 'Q197B6' "$WORK/ultra.tsv"
grep -q 'Q197B6' "$WORK/jackhmmer.tbl"
printf 'ultra_result=\n' >>"$OUT"
cat "$WORK/ultra.tsv" >>"$OUT"
echo 'PASS: default and --more-sensitive gave no rows; --ultra-sensitive and jackhmmer recovered Q197B6.' >>"$OUT"
