#!/usr/bin/env bash
# Regression of prior Input 2: safety gate for dropout versus enrichment interpretation.
set -euo pipefail
PY='F:/OpenScience/audit-envs/crispr-screen-analyst/Scripts/python.exe'
"$PY" interpret_bagel.py canonical_bayes_factor.txt --screen-type dropout -o calls_dropout.tsv 2> dropout.stderr
"$PY" interpret_bagel.py canonical_bayes_factor.txt --screen-type enrichment -o calls_enrichment.tsv 2> enrichment.stderr
"$PY" assert_interpretation.py
