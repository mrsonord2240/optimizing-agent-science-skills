#!/usr/bin/env bash
# Validate canonical JSON schema shape, arithmetic, and final-pass metadata.
set -euo pipefail

audit_root=/mnt/openscience/audits/bio-pathway-go-enrichment
python3 "$audit_root/run/validate_phase2_report.py" | tee "$audit_root/run/validate_phase2_report.out"
