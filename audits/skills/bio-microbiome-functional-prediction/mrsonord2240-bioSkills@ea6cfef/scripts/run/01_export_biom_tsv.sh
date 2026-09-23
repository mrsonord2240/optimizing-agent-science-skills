#!/bin/bash
# Re-audit: independent fresh biom->TSV export (own execution, not reused from the original
# audit or the fix pass) to reproduce the biom-TSV comment-line trap on a fresh real export.
set -euo pipefail

WORK=/mnt/openscience/audits/bio-microbiome-functional-prediction/work
cd "$WORK"

eval "$(micromamba shell hook --shell bash)" 2>/dev/null
micromamba activate picrust2

biom convert -i exported-table/feature-table.biom -o exported-table/feature-table.tsv --to-tsv
echo "biom convert EXIT_CODE=$?"
head -3 exported-table/feature-table.tsv
wc -l exported-table/feature-table.tsv
