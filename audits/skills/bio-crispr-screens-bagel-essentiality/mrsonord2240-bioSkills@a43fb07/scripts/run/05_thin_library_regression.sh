#!/usr/bin/env bash
# Regression of prior Input 6: the supplied 3-sgRNA/gene synthetic library.
set -euo pipefail
PY='F:/OpenScience/audit-envs/crispr-screen-analyst/Scripts/python.exe'
BAGEL='F:/OpenScience/audit-envs/crispr-screen-analyst/tools/dl/bagel/BAGEL.py'
CEG='F:/OpenScience/audit-envs/crispr-screen-analyst/tools/dl/bagel/CEGv2.txt'
NEG='F:/OpenScience/audit-envs/crispr-screen-analyst/tools/dl/bagel/NEGv1.txt'
"$PY" "$BAGEL" fc -i ../data/HAP1_thin_library_synthetic.txt -o thin_fc -c T0 --min-reads 0
"$PY" "$BAGEL" bf -i thin_fc.foldchange -o thin_bayes_factor.txt -e "$CEG" -n "$NEG" -c T18A,T18B,T18C -s 42 -b -NB 1000
"$PY" assert_thin_library.py
