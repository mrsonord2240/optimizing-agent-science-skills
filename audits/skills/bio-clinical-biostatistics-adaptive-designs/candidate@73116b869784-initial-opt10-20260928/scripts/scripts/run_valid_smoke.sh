#!/usr/bin/env bash
set -euo pipefail

root=/mnt/openscience/audit-envs/bio-clinical-biostatistics-adaptive-designs
export PATH="$root/conda-env/bin:$PATH"
export CONDA_PREFIX="$root/conda-env"
timeout 600 "$root/conda-env/bin/Rscript" "$root/tools/smoke_valid_apis.R" \
  > "$root/evidence/valid-api-smoke.log" 2>&1
