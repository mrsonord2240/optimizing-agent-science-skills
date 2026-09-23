.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
Sys.setenv(BASILISK_EXTERNAL_DIR = "F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/cache/basilisk")

h5ad <- "F:/OpenScience/audits/bio-single-cell-data-io/data/ra1_rich.h5ad"

cat("=== zellkonverter readH5AD(reader='R', raw=TRUE) -- regression baseline, should still be broken ===\n")
library(zellkonverter)
library(SingleCellExperiment)
sce_zk <- readH5AD(h5ad, reader = "R", raw = TRUE)
cat("dim:", dim(sce_zk), "\n")
cat("altExpNames:", altExpNames(sce_zk), "| length:", length(altExpNames(sce_zk)), "\n")
cat("assayNames:", assayNames(sce_zk), "\n")

cat("\n=== schard::h5ad2sce(use.raw=TRUE) -- fix's claimed reliable route ===\n")
library(schard)
sce_raw <- schard::h5ad2sce(h5ad, use.raw = TRUE)
cat("dim (use.raw=TRUE):", dim(sce_raw), "\n")
cat("assayNames:", SummarizedExperiment::assayNames(sce_raw), "\n")

sce_hvg <- schard::h5ad2sce(h5ad, use.raw = FALSE)
cat("dim (use.raw=FALSE):", dim(sce_hvg), "\n")

cat("\n=== sanity: does schard's raw recovery carry real values, not just the right shape? ===\n")
# spot-check: sum of first row of recovered raw log-norm X vs the same computed directly from
# the source h5ad's raw/X via python-independent numeric path is out of scope here (cross-language),
# but we can at least confirm the recovered matrix is not all-zero / all-NA, which a shape-only bug
# could still produce.
m <- SummarizedExperiment::assay(sce_raw, "X")
cat("recovered raw X: any non-zero?", any(m != 0), "| dim:", dim(m), "\n")
cat("recovered raw X: any NA?", any(is.na(m@x)), "\n")
