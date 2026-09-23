#!/usr/bin/env bash
# Canonical SIRIUS 6 chain copied from SKILL.md; intentionally not executed because this environment has no SIRIUS login.
set -euo pipefail
sirius --input features.mgf --project ./sirius_project formulas --profile orbitrap fingerprints structures --database bio canopus write-summaries --output ./sirius_summary
