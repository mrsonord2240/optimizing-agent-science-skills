#!/usr/bin/env bash
# Step 3 of the Skill's examples/magma_genebased.sh: gene-set enrichment.
# Executed for real -- FAILED with MAGMA's own clear error, not a crash:
#   "ERROR: insufficient degrees of freedom to run analyses; aborting analysis of
#    remaining models"
# Real cause (confirmed by inspection): MAGMA's gene-set regression conditions on 6
# internal covariates (gene size, log(gene size), gene density, log(gene density),
# inverse MAC, log(inverse MAC)). Our synthetic locus has only 5 genes -- fewer than
# the covariates -- so the regression is structurally unidentifiable. This is a scale
# mismatch (locus-level test data vs a genome-wide ~20k-gene design), not a Skill or
# MAGMA defect, but the Skill's example script and SKILL.md do not state a minimum
# gene-count for this step. See recommendations (P1) in the eval report.
set -euo pipefail
MAGMA="F:/OpenScience/audit-envs/mendelian-randomization-analyst/tools/magma/magma.exe"

"$MAGMA" --gene-results magma_gene.genes.raw \
    --set-annot synthetic_geneset.gmt \
    --out magma_geneset
# (exits 1 as documented above; intentionally left un-worked-around to record the
#  real failure mode)
