#!/usr/bin/env bash
# Regression of prior Input 1: real HAP1 TKOv3 fc -> guarded bf -> pr.
set -euo pipefail
PY='F:/OpenScience/audit-envs/crispr-screen-analyst/Scripts/python.exe'
BAGEL='F:/OpenScience/audit-envs/crispr-screen-analyst/tools/dl/bagel/BAGEL.py'
DATA='../data/HAP1_TKOv3_reads.txt'
CEG='F:/OpenScience/audit-envs/crispr-screen-analyst/tools/dl/bagel/CEGv2.txt'
NEG='F:/OpenScience/audit-envs/crispr-screen-analyst/tools/dl/bagel/NEGv1.txt'
TREAT='HAP1_T18A,HAP1_T18B,HAP1_T18C'
"$PY" "$BAGEL" fc -i "$DATA" -o canonical_fc -c HAP1_T0 --min-reads 30
"$PY" check_bagel_inputs.py pre canonical_fc.foldchange "$CEG" "$NEG" "$TREAT"
"$PY" "$BAGEL" bf -i canonical_fc.foldchange -o canonical_seed_a.txt -e "$CEG" -n "$NEG" -c "$TREAT" -s 42
"$PY" "$BAGEL" bf -i canonical_fc.foldchange -o canonical_seed_b.txt -e "$CEG" -n "$NEG" -c "$TREAT" -s 42
cmp canonical_seed_a.txt canonical_seed_b.txt
cp canonical_seed_a.txt canonical_bayes_factor.txt
"$PY" check_bagel_inputs.py post canonical_bayes_factor.txt
"$PY" "$BAGEL" pr -i canonical_bayes_factor.txt -o canonical_precision_recall.txt -e "$CEG" -n "$NEG"
"$PY" assert_canonical.py
