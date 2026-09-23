#!/usr/bin/env bash
set -euo pipefail
"/f/OpenScience/audit-envs/crispr-screen-analyst/r.sh" scripts/bridge_layout.R samples60.csv 4 16 16 condition,site layout60.csv 10000 17
