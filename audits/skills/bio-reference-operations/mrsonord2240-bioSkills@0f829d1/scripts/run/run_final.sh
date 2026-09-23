#!/usr/bin/env bash
# Reproducible launcher; its log is the assertion evidence for the final pass.
set -euo pipefail
ROOT=/mnt/openscience/audits/bio-reference-operations/run
bash "$ROOT/final_reference_operations.sh" 2>&1 | tee "$ROOT/final_reference_operations.log"
