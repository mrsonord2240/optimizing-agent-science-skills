#!/usr/bin/env bash
# Execute saved Phase 2 input 5 in the isolated R runtime.
set -euo pipefail

audit_root=/mnt/openscience/audits/bio-pathway-go-enrichment
rscript=/home/sci/openscience-go-audit-20260923/bin/Rscript
"$rscript" "$audit_root/run/phase2_input5_custom.R" | tee "$audit_root/run/phase2_input5_custom.out"
