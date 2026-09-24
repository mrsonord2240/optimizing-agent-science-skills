#!/usr/bin/env bash
# Purpose: measure the revised Python validator on 5.6 million primary records without a per-read MAPQ list.
# Inputs: public human BAM repeated 1,000 times; Usage: bash 04_memory_scaling.sh
set -euo pipefail

ROOT=/mnt/openscience
SKILL="$ROOT/worktrees/bio-alignment-validation-finalpass/alignment-files/alignment-validation"
PUBLIC="$ROOT/audit-envs/alignment-files/public-data/human/test.paired_end.sorted.bam"
WORK="$ROOT/audits/bio-alignment-validation/run/finalpass-20260924/data"
OUT="$ROOT/audits/bio-alignment-validation/run/finalpass-20260924/out"
LIST="$WORK/repeat-1000.list"
BIG="$WORK/repeat-1000.bam"

awk -v bam="$PUBLIC" 'BEGIN { for (i = 0; i < 1000; i++) print bam }' > "$LIST"
samtools cat -b "$LIST" -o "$BIG"
samtools quickcheck -v "$BIG"
/usr/bin/time -f 'max_rss_kb=%M elapsed_seconds=%e' \
    python "$SKILL/examples/validate_alignment.py" "$BIG" \
    > "$OUT/memory-scaling.py.out" 2> "$OUT/memory-scaling.py.err"
grep -q 'Mapped: 5640000 (99.96%)' "$OUT/memory-scaling.py.out"
grep -q 'All metrics within normal range' "$OUT/memory-scaling.py.out"
