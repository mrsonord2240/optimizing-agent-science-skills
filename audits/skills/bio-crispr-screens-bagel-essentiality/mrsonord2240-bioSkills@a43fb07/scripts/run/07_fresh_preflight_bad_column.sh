#!/usr/bin/env bash
# Fresh input A: an analyst mistypes a treatment-column header; checker must prevent bf.
set -euo pipefail
PY='F:/OpenScience/audit-envs/crispr-screen-analyst/Scripts/python.exe'
CEG='F:/OpenScience/audit-envs/crispr-screen-analyst/tools/dl/bagel/CEGv2.txt'
NEG='F:/OpenScience/audit-envs/crispr-screen-analyst/tools/dl/bagel/NEGv1.txt'
if "$PY" check_bagel_inputs.py pre canonical_fc.foldchange "$CEG" "$NEG" HAP1_T18A,HAP1_T18B,TYPO_T18C; then
  echo 'ERROR: checker accepted missing column' >&2
  exit 1
fi
echo 'PASS fresh input: missing treatment column rejected before BAGEL invocation'
