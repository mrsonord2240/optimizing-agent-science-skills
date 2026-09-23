#!/usr/bin/env bash
# Confirm whether the shipped all-NA guard rejects a deliberately incompatible DADA2 reference.
set -euo pipefail
BASE='/f/OpenScience/audits/bio-microbiome-taxonomy-assignment'
ENV='/f/OpenScience/audit-envs/microbiome-metagenomics-analyst'
SKILL='/f/OpenScience/wt/microbiome-taxonomy-assignment/microbiome/taxonomy-assignment'
bash "$ENV/rr.sh" "$SKILL/examples/assign_silva.R" \
  "$BASE/data/2026-09-23-final-pass/moving_pictures_770_seqtab.rds" \
  "$BASE/data/2026-09-23-final-pass/bad_reference.fasta" \
  "$BASE/data/2026-09-23-final-pass/nonexistent_species.fasta" \
  "$BASE/data/2026-09-23-final-pass/dada2_bad_reference_taxonomy.rds" rerun
