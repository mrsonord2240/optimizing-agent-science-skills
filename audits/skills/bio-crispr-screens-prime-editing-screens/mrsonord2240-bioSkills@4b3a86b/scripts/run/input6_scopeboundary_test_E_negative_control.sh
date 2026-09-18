#!/usr/bin/env bash
# Re-audit input 6 (Scope Boundary) -- 2026-09-18
# Negative control, deliberately going OUTSIDE the fixed recipe (skipping its own mkdir
# step) to confirm the two pre-fix defects this pass targets are (a) genuinely real on
# this exact PRIDICT2/environment and (b) genuinely absent once the fix's mkdir/pre-create
# steps are followed. This is the before/after evidence for the fix log's two P1 claims.
set -e
PY="F:/OpenScience/audit-envs/crispr-screen-analyst/tools/pridict2-venv/Scripts/python.exe"
SCRIPT="F:/OpenScience/audit-envs/crispr-screen-analyst/tools/dl/PRIDICT2/pridict2_pegRNA_design.py"
DATA_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../data" && pwd)"

WORKDIR="$(mktemp -d)"
cd "$WORKDIR"
echo "Clean working dir: $WORKDIR"
cp "$DATA_DIR/testA_variants.csv" variants.csv

echo "=== Sub-case 1: no input/, no predictions/ dir at all ==="
set +e
"$PY" "$SCRIPT" batch --input-fname variants.csv --output-dir predictions/ --cores 2 --summarize K562
echo "exit code: $?"
set -e
ls -la

echo
echo "=== Sub-case 2: predictions/ created, input/ still missing ==="
mkdir -p predictions
set +e
"$PY" "$SCRIPT" batch --input-fname variants.csv --output-dir predictions/ --cores 2 --summarize K562
echo "exit code: $?"
set -e

echo
echo "=== Sub-case 3: both dirs now created + CSV moved in (the fix's own steps) -- should now succeed ==="
mkdir -p input
mv variants.csv input/
"$PY" "$SCRIPT" batch --input-fname variants.csv --output-dir predictions/ --cores 2 --summarize K562
ls -la predictions/
