# Phase-2 Input 5: separately exercise raw recovery and schard's documented counts-layer tradeoff.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
library(schard)
path <- 'F:/OpenScience/audits/bio-single-cell-data-io/data/fp2_rich.h5ad'
raw <- schard::h5ad2sce(path, use.raw=TRUE)
hvg <- schard::h5ad2sce(path, use.raw=FALSE)
cat('raw_dim', paste(dim(raw), collapse='x'), 'hvg_dim', paste(dim(hvg), collapse='x'), 'hvg_assays', paste(SummarizedExperiment::assayNames(hvg), collapse=','), '\n')
stopifnot(identical(dim(raw), c(33538L,1222L)), identical(dim(hvg), c(700L,1222L)), !('counts' %in% SummarizedExperiment::assayNames(hvg)))
cat('PASS input5\n')
