# Input 5 (Stress) continuation - does schard's use.raw=TRUE recover the raw snapshot
# that zellkonverter's raw=TRUE silently failed to load (input3b)? And confirm layers
# handling is consistent.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
library(schard)

h5ad <- "F:/OpenScience/audits/bio-single-cell-data-io/data/input3_rich.h5ad"

sce_raw <- schard::h5ad2sce(h5ad, use.raw = TRUE)
cat("use.raw=TRUE dim (expect raw shape 33538 x 1222 if raw honored):", paste(dim(sce_raw), collapse=" x "), "\n")
cat("assayNames:", paste(SummarizedExperiment::assayNames(sce_raw), collapse=", "), "\n")

sce_norm <- schard::h5ad2sce(h5ad, use.raw = FALSE)
cat("\nuse.raw=FALSE dim (expect HVG shape 500 x 1222):", paste(dim(sce_norm), collapse=" x "), "\n")
cat("assayNames:", paste(SummarizedExperiment::assayNames(sce_norm), collapse=", "), "\n")
