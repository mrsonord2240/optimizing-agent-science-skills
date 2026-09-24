#!/usr/bin/env bash
# Parse the completed ssGSEA artifacts after the command has published all four GCTs.
set -euo pipefail
PY='F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/Scripts/python.exe'
"$PY" ptmsea.py read --prefix in7_ptmsea/run --out in7_ptmsea_scores.csv > in7_read_after_completion.out 2>&1
