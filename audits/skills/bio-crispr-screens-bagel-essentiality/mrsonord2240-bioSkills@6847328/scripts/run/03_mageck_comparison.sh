#!/bin/bash
# Input 4 (Variant B, regression): BAGEL2 vs MAGeCK Jaccard comparison.
set -e
export PATH="/f/OpenScience/audit-envs/crispr-screen-analyst/tools/dl/mageck-0.5.9.5/bin:$PATH"
PY="F:/OpenScience/audit-envs/crispr-screen-analyst/Scripts/python.exe"

"$PY" "F:/OpenScience/audit-envs/crispr-screen-analyst/Scripts/mageck" test \
    -k HAP1_TKOv3_reads.txt -t HAP1_T18A,HAP1_T18B,HAP1_T18C -c HAP1_T0 -n mageck_hap1

"$PY" jaccard.py
