#!/usr/bin/env bash
# Fresh execution of the shipped SCEPTRE file-input path.
set -euo pipefail
/f/OpenScience/audit-envs/crispr-screen-analyst/r.sh \
  /f/OpenScience/audits/bio-crispr-screens-perturb-seq-analysis/run/shipped_run_sceptre.R \
  /f/OpenScience/audits/bio-crispr-screens-perturb-seq-analysis/data/sceptre_file_input.rds \
  /f/OpenScience/audits/bio-crispr-screens-perturb-seq-analysis/data/sceptre_file_results.tsv
