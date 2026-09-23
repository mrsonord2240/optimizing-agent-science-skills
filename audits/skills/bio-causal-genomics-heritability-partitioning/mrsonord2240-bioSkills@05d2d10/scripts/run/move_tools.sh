#!/bin/bash
set -euo pipefail
SRC_ROOT=/mnt/openscience/audits/bio-causal-genomics-heritability-partitioning/run/tools
DEST_ROOT=/mnt/openscience/audit-envs/mendelian-randomization-analyst/tools
mkdir -p "$DEST_ROOT"
rm -rf "$DEST_ROOT/ldsc-cbiit-reaudit-fresh" "$DEST_ROOT/ldak-reaudit"
mv "$SRC_ROOT/ldsc-fresh" "$DEST_ROOT/ldsc-cbiit-reaudit-fresh"
mv "$SRC_ROOT/ldak" "$DEST_ROOT/ldak-reaudit"
echo "Moved. New sizes:"
du -sh "$DEST_ROOT/ldsc-cbiit-reaudit-fresh" "$DEST_ROOT/ldak-reaudit"
echo "Remaining in run/tools:"
ls -la "$SRC_ROOT"
