#!/bin/bash
# Phase 2 Input 11 (new): run the shipped self-contained normalization example exactly as documented.
set -euo pipefail
/f/OpenScience/audit-envs/untargeted-metabolomics-analyst/rs.sh \
  /f/OpenScience/wt/metabolomics-normalization-qc/metabolomics/normalization-qc/examples/normalize_data.R
