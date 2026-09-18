#!/usr/bin/env bash
# Re-audit input 5 (Stress) -- 2026-09-18
# Robustness check approximating "run --summarize before any real prediction exists":
# the CLI has no standalone summarize-only mode, so this constructs a batch input whose
# single variant has NO NGG PAM within the CLI's search window. The batch step then
# completes with zero successful pegRNA designs, and --summarize runs against an
# output directory that ends up with no per-sequence prediction CSVs at all.
set -e
PY="F:/OpenScience/audit-envs/crispr-screen-analyst/tools/pridict2-venv/Scripts/python.exe"
SCRIPT="F:/OpenScience/audit-envs/crispr-screen-analyst/tools/dl/PRIDICT2/pridict2_pegRNA_design.py"
DATA_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../data" && pwd)"

WORKDIR="$(mktemp -d)"
cd "$WORKDIR"
echo "Clean working dir: $WORKDIR"

mkdir -p input predictions
cp "$DATA_DIR/testD_nopam.csv" input/variants.csv

"$PY" "$SCRIPT" batch \
    --input-fname variants.csv \
    --output-dir predictions/ \
    --cores 1 \
    --summarize K562

echo "--- predictions/ contents (expect summary CSV only, no per-sequence CSV) ---"
ls -la predictions/
cat predictions/*summary*.csv
