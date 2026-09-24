# Input 1 follow-up - determinism of the prescribed scDblFinder call (SKILL.md:81)
# How much do the doublet CALLS (not just labels) move between identically seeded runs?
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({library(scDblFinder); library(SingleCellExperiment); library(Seurat)})

D <- 'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
mats <- list()
for (s in paste0('S', 1:8)) {
  m <- Read10X(file.path(D, s, 'outs/filtered_feature_bc_matrix'))
  colnames(m) <- paste0(s, '_', colnames(m)); mats[[s]] <- m
}
counts <- do.call(cbind, mats); sample_id <- sub('_.*', '', colnames(counts))

run <- function(seed = NULL, bp = NULL) {
  if (!is.null(seed)) set.seed(seed)
  sce <- SingleCellExperiment(list(counts = counts))
  args <- list(sce, samples = sample_id)
  if (!is.null(bp)) args$BPPARAM <- bp
  suppressWarnings(suppressMessages(do.call(scDblFinder, args)))$scDblFinder.class == 'doublet'
}

r1 <- run(20260916); r2 <- run(20260916)
cat(sprintf('set.seed(20260916) twice: calls %d vs %d; disagree on %d cells (%.1f%% of the union of calls)\n',
            sum(r1), sum(r2), sum(r1 != r2), 100 * sum(r1 != r2) / sum(r1 | r2)))

bp <- BiocParallel::SerialParam(RNGseed = 20260916)
b1 <- run(NULL, bp); b2 <- run(NULL, bp)
cat(sprintf('BPPARAM = SerialParam(RNGseed=20260916) twice: calls %d vs %d; disagree on %d cells (%.1f%%)\n',
            sum(b1), sum(b2), sum(b1 != b2), 100 * sum(b1 != b2) / max(sum(b1 | b2), 1)))
cat('DONE\n')
