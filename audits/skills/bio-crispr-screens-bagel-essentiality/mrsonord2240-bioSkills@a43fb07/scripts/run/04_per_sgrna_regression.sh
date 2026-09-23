#!/usr/bin/env bash
# Regression of prior Input 5: documented -r output and additive RPS3 contributions.
set -euo pipefail
PY='F:/OpenScience/audit-envs/crispr-screen-analyst/Scripts/python.exe'
BAGEL='F:/OpenScience/audit-envs/crispr-screen-analyst/tools/dl/bagel/BAGEL.py'
CEG='F:/OpenScience/audit-envs/crispr-screen-analyst/tools/dl/bagel/CEGv2.txt'
NEG='F:/OpenScience/audit-envs/crispr-screen-analyst/tools/dl/bagel/NEGv1.txt'
"$PY" "$BAGEL" bf -i canonical_fc.foldchange -o sgrna_bayes_factor.txt -e "$CEG" -n "$NEG" -c HAP1_T18A,HAP1_T18B,HAP1_T18C -s 42 -r
"$PY" assert_per_sgrna.py
