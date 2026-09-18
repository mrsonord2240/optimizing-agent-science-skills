#!/usr/bin/env bash
# Re-audit input 2 (Variant A) -- 2026-09-18
# Robustness check: fixed recipe with a single-row batch CSV, clean directory, --summarize HEK.
set -e
PY="F:/OpenScience/audit-envs/crispr-screen-analyst/tools/pridict2-venv/Scripts/python.exe"
SCRIPT="F:/OpenScience/audit-envs/crispr-screen-analyst/tools/dl/PRIDICT2/pridict2_pegRNA_design.py"
DATA_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../data" && pwd)"

WORKDIR="$(mktemp -d)"
cd "$WORKDIR"
echo "Clean working dir: $WORKDIR"

mkdir -p input predictions
cp "$DATA_DIR/testC_single_variant.csv" input/variants.csv

"$PY" "$SCRIPT" batch \
    --input-fname variants.csv \
    --output-dir predictions/ \
    --cores 1 \
    --summarize HEK

echo "--- predictions/ contents ---"
ls -la predictions/
cat predictions/*summary*.csv
