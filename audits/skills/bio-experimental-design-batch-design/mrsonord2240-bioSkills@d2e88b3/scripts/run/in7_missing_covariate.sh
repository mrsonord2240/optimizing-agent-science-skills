#!/usr/bin/env bash
set -euo pipefail
if "/f/OpenScience/audit-envs/crispr-screen-analyst/r.sh" scripts/assign_batches.R missing_sex.csv 3 8 condition,sex should_not_exist.csv 100 17; then
  echo "FAIL: missing covariate was accepted" >&2
  exit 1
fi
echo "PASS: missing covariate was rejected."
