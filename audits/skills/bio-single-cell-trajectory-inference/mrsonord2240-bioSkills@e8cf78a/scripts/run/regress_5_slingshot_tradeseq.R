#!/usr/bin/env Rscript
# Re-auditor regression, input 5 (Slingshot + tradeSeq), fresh script (not copied from
# the original auditor's), transcribed from the FIXED worktree SKILL.md's "Slingshot
# and Monocle3 (R)" block plus the raw-counts caveat the fix added.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))

suppressPackageStartupMessages({
  library(schard)
  library(SingleCellExperiment)
  library(slingshot)
  library(tradeSeq)
})

h5ad_path <- 'C:/Users/User/AppData/Local/Temp/claude/f--optimizing-agent-science-skills/a17db7c0-9e8e-4d1d-8394-29c143f93c09/scratchpad/sc-traj-reaudit/data/paul15_paga_dpt.h5ad'
sce <- schard::h5ad2sce(h5ad_path)
cat('SCE dims:', dim(sce), '\n')

tab <- table(colData(sce)$leiden, colData(sce)$paul15_clusters)
mep_col <- which(colnames(tab) == '7MEP')
start_clus <- rownames(tab)[which.max(tab[, mep_col])]
cat('leiden cluster most enriched for real MEP progenitor label:', start_clus, '\n')

# --- SKILL.md "Slingshot and Monocle3 (R)" block, Slingshot half, run verbatim ---
sce <- slingshot(sce, clusterLabels = 'leiden', reducedDim = 'X_umap', start.clus = start_clus)
pt <- slingPseudotime(sce)
cat('slingPseudotime matrix dim (cells x lineages):', dim(pt), '\n')
cat('number of lineages detected:', ncol(pt), '\n')

pt_df <- as.data.frame(pt)
pt_df$paul15_clusters <- colData(sce)$paul15_clusters
mep_pt <- mean(pt_df[pt_df$paul15_clusters == '7MEP', 1], na.rm = TRUE)
cat('MEP mean pseudotime on lineage 1:', mep_pt, '\n')
cat('ASSERTION mep_near_start_of_lineage1 (< 0.3 of max):', mep_pt < 0.3 * max(pt[, 1], na.rm = TRUE), '\n')

# --- fixed SKILL.md's raw-counts caveat for tradeSeq::fitGAM ---
raw_sce <- schard::h5ad2sce('C:/Users/User/AppData/Local/Temp/claude/f--optimizing-agent-science-skills/a17db7c0-9e8e-4d1d-8394-29c143f93c09/scratchpad/sc-traj-reaudit/data/paul15_raw.h5ad')
stopifnot(identical(colnames(raw_sce), colnames(sce)))
counts <- assay(raw_sce, 'X')
cat('raw counts matrix dim for tradeSeq:', dim(counts), ' min value:', min(counts), '\n')

# first, confirm the scaled/clustering matrix genuinely fails as the fix's caveat claims
scaled_counts <- assay(sce, 'X')
cat('scaled/clustering matrix min value (expect negative):', min(scaled_counts), '\n')
scaled_fail <- tryCatch({
  fitGAM(counts = as.matrix(scaled_counts[1:50, ]), sds = SlingshotDataSet(sce), nknots = 5, verbose = FALSE)
  'DID NOT FAIL (unexpected)'
}, error = function(e) paste('FAILED as expected:', conditionMessage(e)))
cat('fitGAM on scaled matrix:', scaled_fail, '\n')

set.seed(2)
keep_genes <- sample(seq_len(nrow(counts)), min(300, nrow(counts)))
counts_sub <- counts[keep_genes, ]
storage.mode(counts_sub) <- 'double'

crv <- SlingshotDataSet(sce)
sce_gam <- tryCatch({
  fitGAM(counts = as.matrix(counts_sub), sds = crv, nknots = 5, verbose = FALSE)
}, error = function(e) { cat('fitGAM ERROR:', conditionMessage(e), '\n'); NULL })

if (!is.null(sce_gam)) {
  assocRes <- associationTest(sce_gam)
  n_sig <- sum(assocRes$pvalue < 0.05, na.rm = TRUE)
  cat('tradeSeq associationTest:', n_sig, '/', nrow(assocRes), 'genes significant at p<0.05\n')
  cat('ASSERTION tradeseq_ran_on_raw_counts: TRUE\n')
} else {
  cat('ASSERTION tradeseq_ran_on_raw_counts: FALSE\n')
}

cat('DONE\n')
