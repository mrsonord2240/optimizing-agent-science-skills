#!/usr/bin/env bash
set -euo pipefail
if "/f/OpenScience/audit-envs/crispr-screen-analyst/r.sh" scripts/bridge_layout.R samples60.csv 4 16 17 condition,site invalid_reserved.csv 10000 17; then
  echo "UNEXPECTED_ACCEPT: out-of-range reserved channel was accepted."
else
  echo "PASS: out-of-range reserved channel was rejected."
fi
