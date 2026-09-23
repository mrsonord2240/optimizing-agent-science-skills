#!/usr/bin/env bash
set -euo pipefail
"/f/OpenScience/audit-envs/crispr-screen-analyst/r.sh" scripts/assign_batches.R samples24.csv 3 8 condition,sex layout24_repeat.csv 10000 17
cmp layout24.csv layout24_repeat.csv
echo "PASS: same seed produced byte-identical layout CSV."
