#!/usr/bin/env bash
# PoPS (FinucaneLab/pops, git-cloned fresh for this audit) run against the REAL
# magma_gene.genes.raw / .genes.out produced in step2 above, with a minimal synthetic
# 3-feature matrix (see make_pops_inputs.py) standing in for FinucaneLab's real
# ~50k-feature matrix (multi-GB download, out of scope for this audit).
set -euo pipefail
PY="F:/OpenScience/audit-envs/mendelian-randomization-analyst/venv-pops/Scripts/python.exe"
POPS="F:/OpenScience/audit-envs/mendelian-randomization-analyst/tools/pops/pops.py"

"$PY" "$POPS" \
    --gene_annot_path pops_gene_annot.txt \
    --feature_mat_prefix pops_feat \
    --num_feature_chunks 1 \
    --magma_prefix magma_gene \
    --control_features_path pops_control_features.txt \
    --out_prefix pops_out

# Result: exit 0, real .preds/.coefs/.marginals written. HONEST CAVEAT: with only 5
# genes on a single chromosome, PoPS's held-out-chromosome ridge CV has no held-out
# chromosome to validate against, so RidgeCV degenerates to maximal shrinkage
# (SELECTED_CV_ALPHA = 1e10) and every PoPS_Score collapses to ~0 (no discrimination
# between PCSK9 and decoys). The CODE PATH is verified correct and runnable
# end-to-end (M4 pass); the SCORES from this toy-scale run are not meaningful and are
# not reported as a real PoPS result anywhere in this audit's grading.
