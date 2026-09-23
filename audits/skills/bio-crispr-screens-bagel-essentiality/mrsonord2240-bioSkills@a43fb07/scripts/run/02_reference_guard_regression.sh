#!/usr/bin/env bash
# Regression of prior Input 3, now checking the shipped pre/post guards.
set -euo pipefail
PY='F:/OpenScience/audit-envs/crispr-screen-analyst/Scripts/python.exe'
BAGEL='F:/OpenScience/audit-envs/crispr-screen-analyst/tools/dl/bagel/BAGEL.py'
CEG='F:/OpenScience/audit-envs/crispr-screen-analyst/tools/dl/bagel/CEGv2.txt'
NEG='F:/OpenScience/audit-envs/crispr-screen-analyst/tools/dl/bagel/NEGv1.txt'
MOUSE='F:/OpenScience/audit-envs/crispr-screen-analyst/tools/dl/bagel/CEG_mouse.txt'
TREAT='HAP1_T18A,HAP1_T18B,HAP1_T18C'
if "$PY" check_bagel_inputs.py pre canonical_fc.foldchange "$MOUSE" "$NEG" "$TREAT"; then exit 1; else echo 'PASS mouse species mismatch blocked before BAGEL'; fi
"$PY" "$BAGEL" bf -i canonical_fc.foldchange -o swapped_bayes_factor.txt -e "$NEG" -n "$CEG" -c "$TREAT" -s 42
if "$PY" check_bagel_inputs.py post swapped_bayes_factor.txt; then exit 1; else echo 'PASS swapped references blocked after BAGEL'; fi
"$PY" assert_reference_guards.py
