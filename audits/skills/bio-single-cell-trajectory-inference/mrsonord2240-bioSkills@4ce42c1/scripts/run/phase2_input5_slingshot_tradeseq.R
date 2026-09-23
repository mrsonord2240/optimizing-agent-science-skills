#!/usr/bin/env Rscript
# Phase 2 Input 5: Slingshot plus tradeSeq, including the raw-counts safeguard.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({ library(schard); library(SingleCellExperiment); library(slingshot); library(tradeSeq) })
root <- 'F:/OpenScience/audits/_pre-fix-20260919/bio-single-cell-trajectory-inference/data'
sce <- schard::h5ad2sce(file.path(root, 'paul15_paga_dpt.h5ad'))
tab <- table(colData(sce)$leiden, colData(sce)$paul15_clusters)
start <- rownames(tab)[which.max(tab[, '7MEP'])]
sce <- slingshot(sce, clusterLabels='leiden', reducedDim='X_umap', start.clus=start)
pt <- slingPseudotime(sce)
mep <- mean(pt[colData(sce)$paul15_clusters == '7MEP', 1], na.rm=TRUE)
near_start <- mep < 0.3 * max(pt[, 1], na.rm=TRUE)
raw <- schard::h5ad2sce(file.path(root, 'paul15_raw.h5ad'))
stopifnot(identical(colnames(raw), colnames(sce)))
raw_counts <- assay(raw, 'X')
scaled <- assay(sce, 'X')
scaled_message <- tryCatch({ fitGAM(counts=as.matrix(scaled[1:30, ]), sds=SlingshotDataSet(sce), nknots=5, verbose=FALSE); 'UNEXPECTED_SUCCESS' }, error=function(e) conditionMessage(e))
set.seed(23)
keep <- sample(seq_len(nrow(raw_counts)), min(150, nrow(raw_counts)))
fit <- fitGAM(counts=as.matrix(raw_counts[keep, ]), sds=SlingshotDataSet(sce), nknots=5, verbose=FALSE)
assoc <- associationTest(fit)
cat(sprintf('lineages=%d; MEP_pt=%.4f; scaled_min=%.4f; raw_assoc_rows=%d\n', ncol(pt), mep, min(scaled), nrow(assoc)))
cat(sprintf('scaled_fitGAM_error=%s\n', scaled_message))
cat(sprintf('ASSERTION_raw_counts_required_and_tradeSeq_runs=%s\n', near_start && nrow(assoc) == length(keep)))
