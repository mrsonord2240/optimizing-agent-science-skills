#!/bin/bash
# Input 5 (Stress) — "Pull every annotated RefSeq reference genome for the genus
# Deinococcus, dehydrated, ready for a parallel pull; tell me how many files that is."
# Follows examples/bulk_dehydrated.sh's full 3-step pattern, using a genus small enough
# to keep the real pull bounded instead of "Bacteria" (which the doc's own example uses
# and which would be a multi-GB, many-thousand-genome pull).
set -euo pipefail
cd "$(dirname "$0")/../work"

DS="/f/OpenScience/audit-envs/database-access/tools/ncbi-datasets-cli/datasets.exe"
TAXON="Deinococcus"

echo "=== Step 1: dehydrated discovery (--reference --annotated --assembly-source RefSeq) ==="
"$DS" download genome taxon "${TAXON}" \
    --reference \
    --annotated \
    --assembly-source RefSeq \
    --include genome,gff3,protein \
    --dehydrated \
    --filename input5_bulk.zip \
    --no-progressbar

rm -rf input5_bulk
unzip -q input5_bulk.zip -d input5_bulk/
FETCH="input5_bulk/ncbi_dataset/fetch.txt"
echo "Files queued: $(wc -l < "$FETCH")"
echo "Columns per row (tab-separated), first 3 rows:"
awk -F'\t' '{print NF}' "$FETCH" | head -3
echo
echo "Genomes in this dehydrated pull:"
find input5_bulk/ncbi_dataset/data -maxdepth 1 -mindepth 1 -type d | sort

echo
echo "=== Step 3 (aria2c substituted with datasets rehydrate — aria2c not in this env, see TOOLS.md) ==="
"$DS" rehydrate --directory input5_bulk/ --max-workers 4 > input5_rehydrate.log 2>&1
tail -5 input5_rehydrate.log
echo
echo "Files after rehydrate: $(find input5_bulk/ncbi_dataset/data -type f | wc -l)"
