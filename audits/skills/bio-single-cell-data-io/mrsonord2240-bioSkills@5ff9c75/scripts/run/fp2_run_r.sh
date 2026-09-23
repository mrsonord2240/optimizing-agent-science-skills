#!/bin/bash
# Runs a saved Phase-2 R test through the audited environment's mandated wrapper.
set -euo pipefail
exec /f/OpenScience/audit-envs/single-cell-transcriptomics-analyst/tools/rs.sh "$1"
