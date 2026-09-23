#!/usr/bin/env bash
# Phase 2 fresh-input preparation. The archived prior audit contributes only the
# immutable public-data-derived inputs; every derived result is written below.
set -euo pipefail
OUT=/mnt/openscience/audits/bio-microbiome-functional-prediction/work/p2-final-20260923
OLD=/mnt/openscience/audits/_pre-fix-20260923/bio-microbiome-functional-prediction/work
mkdir -p "$OUT/exported-table"
cp "$OLD/asv_seqs.fna" "$OUT/asv_seqs.fna"
cp "$OLD/exported-table/feature-table.biom" "$OUT/exported-table/feature-table.biom"
eval "$(micromamba shell hook --shell bash)" 2>/dev/null
micromamba activate picrust2
biom convert -i "$OUT/exported-table/feature-table.biom" -o "$OUT/exported-table/feature-table.tsv" --to-tsv
head -n 2 "$OUT/exported-table/feature-table.tsv"
tail -n +2 "$OUT/exported-table/feature-table.tsv" > "$OUT/asv_table.tsv"
test "$(head -n 1 "$OUT/asv_table.tsv" | cut -f1)" = "#OTU ID"
printf 'prepared_asvs=%s prepared_table_rows=%s\n' "$(grep -c '^>' "$OUT/asv_seqs.fna")" "$(wc -l < "$OUT/asv_table.tsv")"
