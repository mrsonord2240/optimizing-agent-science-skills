#!/bin/bash
# Input 4 (Variant B) — "Find NCBI's ortholog set for human BRCA1 across all species,
# one representative per species, as a TSV."
# Follows usage-guide.md's "NCBI ortholog set" example prompt and SKILL.md's
# "Find orthologs for a gene" code pattern verbatim (bare --ortholog flag).
set -euo pipefail
cd "$(dirname "$0")/../work"

DS="/f/OpenScience/audit-envs/database-access/tools/ncbi-datasets-cli/datasets.exe"
DF="/f/OpenScience/audit-envs/database-access/tools/ncbi-datasets-cli/dataformat.exe"

echo "=== SKILL.md's documented pattern (bare --ortholog flag) ==="
set +e
"$DS" summary gene symbol BRCA1 --taxon human --ortholog --as-json-lines > input4_ortholog_doc.jsonl 2> input4_ortholog_doc.err
DOC_EXIT=$?
set -e
echo "exit code: $DOC_EXIT"
cat input4_ortholog_doc.err

echo
echo "=== Corrected: --ortholog all (explicit value required) ==="
"$DS" summary gene symbol BRCA1 --taxon human --ortholog all --as-json-lines > input4_ortholog_all.jsonl
wc -l input4_ortholog_all.jsonl

echo
echo "=== dataformat tsv gene on the ortholog set ==="
"$DF" tsv gene --inputfile input4_ortholog_all.jsonl \
    --fields gene-id,symbol,tax-name,description | column -t -s $'\t' | head -15
echo "..."
"$DF" tsv gene --inputfile input4_ortholog_all.jsonl \
    --fields gene-id,symbol,tax-name,description | wc -l
