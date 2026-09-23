#!/usr/bin/env bash
set -euo pipefail
if "/f/OpenScience/audit-envs/crispr-screen-analyst/r.sh" scripts/assign_batches.R samples60.csv 3 8 condition,site should_not_exist.csv 100 17; then
  echo "FAIL: over-capacity design was accepted" >&2
  exit 1
fi
echo "PASS: over-capacity design was rejected."
