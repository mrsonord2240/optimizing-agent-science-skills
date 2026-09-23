#!/usr/bin/env bash
# Fresh input B: user needs bootstrap uncertainty and validates documented CLI flags.
set -euo pipefail
PY='F:/OpenScience/audit-envs/crispr-screen-analyst/Scripts/python.exe'
BAGEL='F:/OpenScience/audit-envs/crispr-screen-analyst/tools/dl/bagel/BAGEL.py'
CEG='F:/OpenScience/audit-envs/crispr-screen-analyst/tools/dl/bagel/CEGv2.txt'
NEG='F:/OpenScience/audit-envs/crispr-screen-analyst/tools/dl/bagel/NEGv1.txt'
"$PY" "$BAGEL" fc --help > fc_help.txt
"$PY" "$BAGEL" bf --help > bf_help.txt 2>&1
"$PY" "$BAGEL" pr --help > pr_help.txt
"$PY" "$BAGEL" bf -i canonical_fc.foldchange -o bootstrap_50.txt -e "$CEG" -n "$NEG" -c HAP1_T18A,HAP1_T18B,HAP1_T18C -s 42 -b -NB 50
"$PY" assert_bootstrap_and_help.py
