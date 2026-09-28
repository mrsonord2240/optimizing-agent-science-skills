#!/bin/bash
set -euo pipefail
AUDIT=/mnt/openscience/audits/bio-data-visualization-network-visualization
export MAMBA_ROOT_PREFIX=/home/sci/micromamba
micromamba run -n dv-cli python "$AUDIT/run/wsl_directed_cases.py" \
  2>&1 | tee "$AUDIT/logs/wsl_directed.log"
