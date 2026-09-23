#!/usr/bin/env bash
# Execute the shipped DADA2 example exactly as documented, with fresh audit output paths.
set -euo pipefail
BASE='/f/OpenScience/audits/bio-microbiome-taxonomy-assignment'
ENV='/f/OpenScience/audit-envs/microbiome-metagenomics-analyst'
SKILL='/f/OpenScience/wt/microbiome-taxonomy-assignment/microbiome/taxonomy-assignment'
bash "$ENV/rr.sh" "$SKILL/examples/assign_silva.R" \
  "$BASE/data/2026-09-23-final-pass/moving_pictures_770_seqtab.rds" \
  "$ENV/reaudit-tax/regionmatched_dada2_train.fasta" \
  "$ENV/reaudit-tax/regionmatched_dada2_species.fasta" \
  "$BASE/data/2026-09-23-final-pass/dada2_taxonomy.rds" rerun
