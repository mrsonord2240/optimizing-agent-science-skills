#!/usr/bin/env bash
# Re-audit input 1 (Canonical) -- 2026-09-18
# Follows SKILL.md's FIXED batch-mode recipe verbatim, from a genuinely clean directory
# (no pre-existing input/ or predictions/), on a variant set NOT reused from the fixer's
# own test fixture (deletion + insertion edits, not the fixer's "replacement1" substitution).
set -e
PY="F:/OpenScience/audit-envs/crispr-screen-analyst/tools/pridict2-venv/Scripts/python.exe"
SCRIPT="F:/OpenScience/audit-envs/crispr-screen-analyst/tools/dl/PRIDICT2/pridict2_pegRNA_design.py"
DATA_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../data" && pwd)"

WORKDIR="$(mktemp -d)"
cd "$WORKDIR"
echo "Clean working dir: $WORKDIR"

# --- exactly as SKILL.md's fixed recipe documents it ---
mkdir -p input predictions
cp "$DATA_DIR/testA_variants.csv" input/variants.csv

"$PY" "$SCRIPT" batch \
    --input-fname variants.csv \
    --output-dir predictions/ \
    --cores 2 \
    --summarize K562

echo "--- predictions/ contents ---"
ls -la predictions/
echo "--- summary CSV ---"
cat predictions/*summary*.csv
