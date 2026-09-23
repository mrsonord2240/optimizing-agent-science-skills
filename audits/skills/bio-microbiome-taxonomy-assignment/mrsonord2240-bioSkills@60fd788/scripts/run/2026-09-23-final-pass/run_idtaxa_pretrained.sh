#!/usr/bin/env bash
# Execute the shipped IDTAXA script exactly as documented against a real pre-trained SILVA slice.
set -euo pipefail
BASE='/f/OpenScience/audits/bio-microbiome-taxonomy-assignment'
ENV='/f/OpenScience/audit-envs/microbiome-metagenomics-analyst'
SKILL='/f/OpenScience/wt/microbiome-taxonomy-assignment/microbiome/taxonomy-assignment'
bash "$ENV/rr.sh" "$SKILL/scripts/idtaxa_classify.R" \
  "$BASE/data/2026-09-23-final-pass/moving_pictures_770_seqtab.rds" \
  "$ENV/reaudit-tax/trainingSet.rds" \
  "$BASE/data/2026-09-23-final-pass/idtaxa_pretrained.rds" rerun
