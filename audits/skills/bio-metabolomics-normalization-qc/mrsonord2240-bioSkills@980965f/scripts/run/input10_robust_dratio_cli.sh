#!/bin/bash
# Phase 2 Input 10: invoke the Skill's documented robust D-ratio CLI after its preparation run.
set -euo pipefail
/f/OpenScience/audit-envs/untargeted-metabolomics-analyst/rs.sh \
  /f/OpenScience/wt/metabolomics-normalization-qc/metabolomics/normalization-qc/scripts/robust_dratio_filter.R \
  /f/OpenScience/audits/bio-metabolomics-normalization-qc/run/input10_peaks.csv \
  /f/OpenScience/audits/bio-metabolomics-normalization-qc/run/input10_kept.csv sample_type QC 0.5 0.3
/f/OpenScience/audit-envs/untargeted-metabolomics-analyst/rs.sh \
  /f/OpenScience/audits/bio-metabolomics-normalization-qc/run/input10_robust_dratio_verify.R
