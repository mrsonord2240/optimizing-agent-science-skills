#!/usr/bin/env bash
set -euo pipefail
ROOT=/mnt/openscience/audits/bio-reference-operations/run
python "$ROOT/validate_report.py" 2>&1 | tee "$ROOT/validate_report.log"
