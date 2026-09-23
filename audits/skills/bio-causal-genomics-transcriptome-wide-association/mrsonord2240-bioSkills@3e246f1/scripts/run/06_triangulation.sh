#!/usr/bin/env bash
# Execute the final-pass cis-eQTL MR plus coloc triangulation fixture.
set -euo pipefail
'/f/OpenScience/audit-envs/mendelian-randomization-analyst/r.sh' \
  '/f/OpenScience/audits/bio-causal-genomics-transcriptome-wide-association/run/06_triangulation.R'
