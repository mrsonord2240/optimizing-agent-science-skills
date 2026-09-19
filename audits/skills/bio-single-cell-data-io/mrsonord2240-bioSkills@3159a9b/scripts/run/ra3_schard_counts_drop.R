# New input beyond the fixer's verification: reproduce the P2 claim
# ("schard reads X only -- does not carry a counts layer") on this re-auditor's
# own independently-built h5ad (ra1_rich.h5ad, which has a real counts layer),
# not the fixer's or original auditor's file.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
library(schard)

h5ad <- "F:/OpenScience/audits/bio-single-cell-data-io/data/ra1_rich.h5ad"
sce <- schard::h5ad2sce(h5ad, use.raw = FALSE)
cat("assayNames:", SummarizedExperiment::assayNames(sce), "\n")
cat("counts layer present?", "counts" %in% SummarizedExperiment::assayNames(sce), "\n")
