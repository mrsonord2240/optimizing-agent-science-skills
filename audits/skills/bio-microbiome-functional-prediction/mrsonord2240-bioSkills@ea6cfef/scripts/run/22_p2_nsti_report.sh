#!/usr/bin/env bash
# Run the shipped NSTI reporter verbatim against the fresh central output.
set -euo pipefail
OUT=/mnt/openscience/audits/bio-microbiome-functional-prediction/work/p2-final-20260923
cd /mnt/openscience/wt/microbiome-functional-prediction/microbiome/functional-prediction
eval "$(micromamba shell hook --shell bash)" 2>/dev/null
micromamba activate picrust2-263-p2
python3 scripts/nsti_report.py "$OUT/picrust2_out_documented" "$OUT/asv_table.tsv" --max-nsti 2.0
python3 scripts/nsti_report.py "$OUT/picrust2_out_documented" "$OUT/asv_table.tsv" --max-nsti 0.5
