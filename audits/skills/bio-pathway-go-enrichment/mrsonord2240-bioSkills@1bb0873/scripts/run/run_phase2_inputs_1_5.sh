#!/usr/bin/env bash
# Execute Phase 2 inputs 1-5 in the isolated Bioconductor 3.20 R runtime.
set -euo pipefail

audit_root=/mnt/openscience/audits/bio-pathway-go-enrichment
rscript=/home/sci/openscience-go-audit-20260923/bin/Rscript
"$rscript" "$audit_root/run/phase2_inputs_1_5.R" | tee "$audit_root/run/phase2_inputs_1_5.out"
