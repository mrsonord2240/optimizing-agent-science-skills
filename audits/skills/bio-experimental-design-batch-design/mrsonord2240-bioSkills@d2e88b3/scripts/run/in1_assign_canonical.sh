#!/usr/bin/env bash
set -euo pipefail
"/f/OpenScience/audit-envs/crispr-screen-analyst/r.sh" scripts/assign_batches.R samples24.csv 3 8 condition,sex layout24.csv 10000 17
