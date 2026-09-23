#!/usr/bin/env bash
# Syntax/import/CLI checks for every shipped executable at the audited commit.
set -euo pipefail
ROOT='F:/OpenScience'
ENV="$ROOT/audit-envs/mass-spec-proteomics-analyst"
PY="$ENV/Scripts/python.exe"
RSH="$ENV/r.sh"
for py in phospho_analysis.py motif_enrichment.py ptmsea.py; do
  "$PY" -m py_compile "$py"
done
for r in msstatsptm_labelfree.R msstatsptm_tmt.R ksea_scores.R; do
  "$RSH" -e "parse(file='$r')"
done
"$PY" motif_enrichment.py --help
"$PY" ptmsea.py --help
