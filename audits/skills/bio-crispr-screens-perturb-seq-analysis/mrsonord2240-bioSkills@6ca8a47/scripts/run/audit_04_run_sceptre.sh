#!/usr/bin/env bash
# Fresh execution of the shipped SCEPTRE example path via the required audit R wrapper.
set -euo pipefail
/f/OpenScience/audit-envs/crispr-screen-analyst/r.sh \
  /f/OpenScience/audits/bio-crispr-screens-perturb-seq-analysis/run/shipped_run_sceptre.R \
  --example \
  /f/OpenScience/audits/bio-crispr-screens-perturb-seq-analysis/data/sceptre_example.tsv
