#!/usr/bin/env Rscript
# Input 5 (Stress / complex / multi-part) -- "I have a Seurat object already
# clustered by cell type; fit Slingshot lineage curves from the progenitor
# start cluster, then run tradeSeq to find genes changing along pseudotime",
# following SKILL.md's "Slingshot and Monocle3 (R)" code block (Slingshot
# half) plus the documented tradeSeq follow-up (fitGAM + associationTest),
# on the same real Paul15 myeloid/erythroid progenitor data used for
# Inputs 1-2 (exported from Python with PCA/UMAP/leiden already computed).
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))

suppressPackageStartupMessages({
  library(schard)
  library(SingleCellExperiment)
  library(slingshot)
  library(tradeSeq)
})

h5ad_path <- 'F:/OpenScience/audits/bio-single-cell-trajectory-inference/data/paul15_paga_dpt.h5ad'
sce <- schard::h5ad2sce(h5ad_path)
cat('SCE dims:', dim(sce), '\n')
cat('assays:', assayNames(sce), '\n')
cat('reducedDims:', reducedDimNames(sce), '\n')
cat('colData cols:', colnames(colData(sce)), '\n')

# find which leiden cluster is dominated by the real MEP progenitor label
tab <- table(colData(sce)$leiden, colData(sce)$paul15_clusters)
mep_col <- which(colnames(tab) == '7MEP')
start_clus <- rownames(tab)[which.max(tab[, mep_col])]
cat('\nleiden cluster most enriched for real MEP progenitor label:', start_clus, '\n')
cat('cross-tab (leiden x paul15_clusters), MEP column:\n')
print(tab[, mep_col])

# --- SKILL.md "Slingshot and Monocle3 (R)" block, Slingshot half, run verbatim ---
sce <- slingshot(sce, clusterLabels = 'leiden', reducedDim = 'X_umap', start.clus = start_clus)
pt <- slingPseudotime(sce)
cat('\nslingPseudotime matrix dim (cells x lineages):', dim(pt), '\n')
cat('number of lineages detected:', ncol(pt), '\n')

# ground-truth check: mean pseudotime per real cell type, per lineage
pt_df <- as.data.frame(pt)
pt_df$paul15_clusters <- colData(sce)$paul15_clusters
for (lin in colnames(pt)) {
  cat('\n--- Lineage', lin, '---\n')
  agg <- aggregate(pt_df[[lin]], by = list(cluster = pt_df$paul15_clusters), FUN = function(x) mean(x, na.rm = TRUE))
  agg <- agg[order(agg$x), ]
  print(agg)
}

mep_pt <- mean(pt_df[pt_df$paul15_clusters == '7MEP', 1], na.rm = TRUE)
cat('\nMEP mean pseudotime on lineage 1:', mep_pt, '\n')
cat('ASSERTION mep_near_start_of_lineage1 (< 0.3 of max):', mep_pt < 0.3 * max(pt[, 1], na.rm = TRUE), '\n')

# --- tradeSeq follow-up, as SKILL.md text directs ("downstream DE goes
# through tradeSeq (fitGAM then associationTest ... )") ---
# NOTE: the exported h5ad's .X went through the SKILL.md-adjacent
# recipe_zheng17 (log1p + z-scale) upstream for clustering/UMAP -- that
# matrix has negative values and fitGAM correctly refuses it
# ("All values of the count matrix should be non-negative"). tradeSeq's
# NB-GAM needs RAW counts, not the scaled matrix used for embedding. The
# Skill's text names fitGAM/associationTest but never states this input
# must be raw counts, not the same matrix already in hand from the
# UMAP/clustering step -- reloading the untouched raw counts here to
# check whether the method itself works once given the right input.
raw_sce <- schard::h5ad2sce('F:/OpenScience/audits/bio-single-cell-trajectory-inference/data/paul15_raw.h5ad')
stopifnot(identical(colnames(raw_sce), colnames(sce)))
counts <- assay(raw_sce, 'X')
cat('\nraw counts matrix dim for tradeSeq:', dim(counts), ' min value:', min(counts), '\n')

set.seed(1)
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
  cat('\ntradeSeq associationTest: ', n_sig, '/', nrow(assocRes), ' genes significant at p<0.05 (of', length(keep_genes), 'sampled genes)\n')
  cat('ASSERTION tradeseq_fitgam_and_associationtest_ran: TRUE\n')
} else {
  cat('ASSERTION tradeseq_fitgam_and_associationtest_ran: FALSE\n')
}

cat('\nDone.\n')
