#!/usr/bin/env bash
# Re-audit input 4 (Variant B) -- 2026-09-18
# Regression-consistency check: this fix pass only touched the input-dir/output-dir setup
# and the Common Errors table. Confirm the ALREADY-documented "wrong CSV header" failure
# mode (from the 2026-09-16 fix pass) still behaves exactly as SKILL.md describes, i.e.
# the fix did not accidentally alter or paper over it.
set -e
PY="F:/OpenScience/audit-envs/crispr-screen-analyst/tools/pridict2-venv/Scripts/python.exe"
SCRIPT="F:/OpenScience/audit-envs/crispr-screen-analyst/tools/dl/PRIDICT2/pridict2_pegRNA_design.py"
DATA_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../data" && pwd)"

WORKDIR="$(mktemp -d)"
cd "$WORKDIR"
echo "Clean working dir: $WORKDIR"

# dirs correctly pre-created (per the FIXED recipe) -- only the CSV header is wrong
mkdir -p input predictions
cp "$DATA_DIR/testF_wrongcolumn.csv" input/variants.csv

"$PY" "$SCRIPT" batch \
    --input-fname variants.csv \
    --output-dir predictions/ \
    --cores 1 \
    --summarize K562

echo "--- predictions/ contents ---"
ls -la predictions/
echo "--- summary file content (expect '\"\"' + 'Missing editseq column' warning on stdout) ---"
cat predictions/*summary*.csv
