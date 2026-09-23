#!/usr/bin/env bash
# Run the saved static source/scope check for Phase 2 input 7.
set -euo pipefail

audit_root=/mnt/openscience/audits/bio-pathway-go-enrichment
python3 "$audit_root/run/phase2_input7_scope.py" | tee "$audit_root/run/phase2_input7_scope.out"
