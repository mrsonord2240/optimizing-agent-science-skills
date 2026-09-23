#!/usr/bin/env bash
# Exercise the documented five-argument train-from-reference path with a fresh, bounded real SILVA slice.
set -euo pipefail
BASE='/f/OpenScience/audits/bio-microbiome-taxonomy-assignment'
ENV='/f/OpenScience/audit-envs/microbiome-metagenomics-analyst'
SKILL='/f/OpenScience/wt/microbiome-taxonomy-assignment/microbiome/taxonomy-assignment'
bash "$ENV/rr.sh" "$SKILL/scripts/idtaxa_classify.R" \
  "$BASE/data/2026-09-23-final-pass/moving_pictures_770_seqtab.rds" \
  "$BASE/data/2026-09-23-final-pass/idtaxa_small_training.rds" \
  "$BASE/data/2026-09-23-final-pass/idtaxa_trained.rds" \
  "$BASE/data/2026-09-23-final-pass/small_region_reference.fasta" \
  "$BASE/data/2026-09-23-final-pass/small_region_reference_taxonomy.txt" rerun
