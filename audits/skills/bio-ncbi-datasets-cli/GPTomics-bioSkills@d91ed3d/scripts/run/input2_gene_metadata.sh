#!/bin/bash
# Input 2 (Variant A) — "Get a TSV of BRCA1 gene metadata across Mammalia: gene ID,
# symbol, taxon name, description, nomenclature authority symbol, chromosome."
# Follows SKILL.md's "Gene metadata across species" pattern / examples/gene_metadata.sh verbatim.
set -euo pipefail
cd "$(dirname "$0")/../work"

DS="/f/OpenScience/audit-envs/database-access/tools/ncbi-datasets-cli/datasets.exe"
DF="/f/OpenScience/audit-envs/database-access/tools/ncbi-datasets-cli/dataformat.exe"

echo "=== datasets summary gene symbol BRCA1 --taxon Mammalia ==="
"$DS" summary gene symbol BRCA1 --taxon Mammalia --as-json-lines > input2_brca1_mammalia.jsonl
wc -l input2_brca1_mammalia.jsonl

echo
echo "=== dataformat tsv gene, SKILL.md's documented --fields (as written in examples/gene_metadata.sh) ==="
set +e
"$DF" tsv gene --inputfile input2_brca1_mammalia.jsonl \
    --fields gene-id,symbol,taxname,description,chromosomes,nomenclature-authority-symbol
DOC_EXIT=$?
set -e
echo "exit code (doc field names): $DOC_EXIT"

echo
echo "=== dataformat tsv gene, corrected field names ==="
"$DF" tsv gene --inputfile input2_brca1_mammalia.jsonl \
    --fields gene-id,symbol,tax-name,description,chromosomes \
    | column -t -s $'\t'
