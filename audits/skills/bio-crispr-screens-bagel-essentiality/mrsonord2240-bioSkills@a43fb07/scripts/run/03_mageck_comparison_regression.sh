#!/usr/bin/env bash
# Regression of prior Input 4: independently run MAGeCK and compute the Jaccard set overlap.
set -euo pipefail
PY='F:/OpenScience/audit-envs/crispr-screen-analyst/Scripts/python.exe'
MAGECK='F:/OpenScience/audit-envs/crispr-screen-analyst/Scripts/mageck'
export PATH="/f/OpenScience/audit-envs/crispr-screen-analyst/tools/dl/mageck-0.5.9.5/bin:$PATH"
"$PY" "$MAGECK" test -k ../data/HAP1_TKOv3_reads.txt -t HAP1_T18A,HAP1_T18B,HAP1_T18C -c HAP1_T0 -n mageck_hap1
"$PY" assert_mageck_comparison.py
