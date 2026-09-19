#!/bin/bash
# Input 3 (Edge) — "I need to inspect what files a genome download would pull before
# committing the I/O. Use the dehydrated workflow for GCF_000819615.1, show me the
# manifest, then rehydrate it."
# Exercises SKILL.md's "When to use --dehydrated" 3-step pattern and the exact awk
# transform in examples/bulk_dehydrated.sh line 31.
set -euo pipefail
cd "$(dirname "$0")/../work"

DS="/f/OpenScience/audit-envs/database-access/tools/ncbi-datasets-cli/datasets.exe"
ACC="GCF_000819615.1"

echo "=== Step 1: dehydrated discovery ==="
"$DS" download genome accession "${ACC}" \
    --include genome,protein,cds,seq-report \
    --dehydrated \
    --filename input3_dehydrated.zip \
    --no-progressbar

rm -rf input3_dehydrated
unzip -q input3_dehydrated.zip -d input3_dehydrated/
FETCH="input3_dehydrated/ncbi_dataset/fetch.txt"
echo "=== fetch.txt raw ==="
cat -A "$FETCH" | head -5
echo
echo "=== column count per row (tab-separated) ==="
awk -F'\t' '{print NF}' "$FETCH"

echo
echo "=== SKILL.md's documented assumption: <url> [TAB] <path-relative-to-data-dir> (2 cols) ==="
echo "=== examples/bulk_dehydrated.sh line 31's literal transform: awk -F'\\t' '{print \$1\"\\n  out=\"\$2}' ==="
awk -F'\t' '{print $1"\n  out="$2}' "$FETCH"

echo
echo "=== Step 3: verify/pull via datasets rehydrate (the Skill's own documented alternative to aria2c) ==="
"$DS" rehydrate --directory input3_dehydrated/ --max-workers 4
find input3_dehydrated/ncbi_dataset/data -type f
