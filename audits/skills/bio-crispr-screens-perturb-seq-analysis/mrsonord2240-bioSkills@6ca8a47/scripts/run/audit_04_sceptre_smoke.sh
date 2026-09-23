#!/usr/bin/env bash
# Isolate package load/teardown from the shipped analysis script.
set -euo pipefail
/f/OpenScience/audit-envs/crispr-screen-analyst/r.sh \
  /f/OpenScience/audits/bio-crispr-screens-perturb-seq-analysis/run/audit_04_sceptre_smoke.R
