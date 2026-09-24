# Build a Seurat RDS from the focused synthetic h5ad fixture for source-script validation.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({ library(zellkonverter); library(Seurat) })
a <- readH5AD('F:/OpenScience/audits/bio-single-cell-batch-integration/run/re_audit_subset.h5ad', reader = 'R')
counts <- SummarizedExperiment::assay(a, 'X')
obj <- CreateSeuratObject(counts = counts, meta.data = as.data.frame(SummarizedExperiment::colData(a)))
stopifnot(ncol(obj) == 400L, all(c('A', 'B') %in% unique(obj$batch)))
saveRDS(obj, 'F:/OpenScience/audits/bio-single-cell-batch-integration/run/re_audit_subset.rds')
cat(sprintf('prepared Seurat RDS: %d cells, %d genes\n', ncol(obj), nrow(obj)))
