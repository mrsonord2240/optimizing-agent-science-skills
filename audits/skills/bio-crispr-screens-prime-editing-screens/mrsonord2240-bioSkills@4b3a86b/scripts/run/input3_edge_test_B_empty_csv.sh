#!/usr/bin/env bash
# Re-audit input 3 (Edge) -- 2026-09-18
# Robustness check: fixed recipe (dirs correctly pre-created) but the input CSV has a
# correct header and ZERO data rows. Does the CLI crash, hang, or degrade gracefully?
set -e
PY="F:/OpenScience/audit-envs/crispr-screen-analyst/tools/pridict2-venv/Scripts/python.exe"
SCRIPT="F:/OpenScience/audit-envs/crispr-screen-analyst/tools/dl/PRIDICT2/pridict2_pegRNA_design.py"
DATA_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../data" && pwd)"

WORKDIR="$(mktemp -d)"
cd "$WORKDIR"
echo "Clean working dir: $WORKDIR"

mkdir -p input predictions
cp "$DATA_DIR/testB_empty.csv" input/variants.csv

"$PY" "$SCRIPT" batch \
    --input-fname variants.csv \
    --output-dir predictions/ \
    --cores 2 \
    --summarize K562

echo "--- predictions/ contents ---"
ls -la predictions/
echo "--- summary file content (expect known-empty '\"\"' per existing Common Errors row) ---"
cat predictions/*summary*.csv
