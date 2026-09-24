#!/usr/bin/env bash
# Purpose: verify metric-table output without charts and capture the chart/R prerequisite explicitly.
# Inputs: public human BAM and its matching FASTA; Usage: bash 05_picard_contracts.sh
set -uo pipefail

ROOT=/mnt/openscience
PUBLIC="$ROOT/audit-envs/alignment-files/public-data/human"
OUT="$ROOT/audits/bio-alignment-validation/run/finalpass-20260924/out"
BAM="$PUBLIC/test.paired_end.sorted.bam"
REF="$PUBLIC/genome.fasta"

picard CollectInsertSizeMetrics I="$BAM" O="$OUT/insert-no-chart.txt" > "$OUT/insert-no-chart.stdout" 2> "$OUT/insert-no-chart.stderr"
test -s "$OUT/insert-no-chart.txt"
grep -q 'MEDIAN_INSERT_SIZE' "$OUT/insert-no-chart.txt"

picard CollectGcBiasMetrics I="$BAM" O="$OUT/gc-no-chart.txt" S="$OUT/gc-no-chart-summary.txt" R="$REF" > "$OUT/gc-no-chart.stdout" 2> "$OUT/gc-no-chart.stderr"
test -s "$OUT/gc-no-chart.txt"
test -s "$OUT/gc-no-chart-summary.txt"
grep -q 'NORMALIZED_COVERAGE' "$OUT/gc-no-chart.txt"

picard CollectInsertSizeMetrics I="$BAM" O="$OUT/insert-with-chart.txt" H="$OUT/insert-with-chart.pdf" > "$OUT/insert-with-chart.stdout" 2> "$OUT/insert-with-chart.stderr"
chart_rc=$?
printf 'insert_chart_rc=%s rscript=%s\n' "$chart_rc" "$(command -v Rscript || echo absent)" | tee "$OUT/picard-chart-prerequisite.summary"
if [ "$chart_rc" -eq 0 ]; then test -s "$OUT/insert-with-chart.pdf"; else grep -Eiq 'Rscript|R is not installed' "$OUT/insert-with-chart.stderr"; fi
