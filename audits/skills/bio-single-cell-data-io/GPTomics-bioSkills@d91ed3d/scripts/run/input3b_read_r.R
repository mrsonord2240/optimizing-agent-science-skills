# Input 3 (Edge), Step B (R): read the h5ad built in input3a via the two converters
# SKILL.md actually documents as installed alternatives in this environment (anndataR is
# blocked here -- see TOOLS.md -- so we use zellkonverter and schard, both named in
# SKILL.md's own conversion table).
# Check: dims transposed correctly (genes x cells), obsm -> reducedDims, raw -> altExp
# (only if raw=TRUE per SKILL.md's own warning), categorical obs survives.

.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
Sys.setenv(BASILISK_EXTERNAL_DIR = "F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/cache/basilisk")

h5ad <- "F:/OpenScience/audits/bio-single-cell-data-io/data/input3_rich.h5ad"

cat("=== schard::h5ad2sce ===\n")
library(schard)
sce_schard <- schard::h5ad2sce(h5ad)
cat("dim (should be genes x cells = 500 x 1222):", paste(dim(sce_schard), collapse=" x "), "\n")
cat("assayNames:", paste(SummarizedExperiment::assayNames(sce_schard), collapse=", "), "\n")
cat("reducedDimNames:", paste(SingleCellExperiment::reducedDimNames(sce_schard), collapse=", "), "\n")
batch_col <- SummarizedExperiment::colData(sce_schard)$batch
cat("obs batch column class:", class(batch_col), "\n")
cat("obs batch unique values:", paste(unique(as.character(batch_col)), collapse=", "), "\n")

cat("\n=== zellkonverter::readH5AD(reader='R') ===\n")
library(zellkonverter)
sce_zk <- readH5AD(h5ad, reader = "R")
cat("dim (should be genes x cells = 500 x 1222):", paste(dim(sce_zk), collapse=" x "), "\n")
cat("assayNames:", paste(SummarizedExperiment::assayNames(sce_zk), collapse=", "), "\n")
cat("reducedDimNames (X_pca should map here per SKILL.md 'obsm -> reducedDims'):",
    paste(SingleCellExperiment::reducedDimNames(sce_zk), collapse=", "), "\n")
cat("altExpNames (raw should be HERE ONLY if raw=TRUE was passed -- SKILL.md warns default is FALSE):",
    paste(SingleCellExperiment::altExpNames(sce_zk), collapse=", "), "\n")
batch_col_zk <- SummarizedExperiment::colData(sce_zk)$batch
cat("obs batch column class:", class(batch_col_zk), "\n")
cat("obs batch unique values:", paste(unique(as.character(batch_col_zk)), collapse=", "), "\n")

cat("\n=== zellkonverter::readH5AD(reader='R', raw=TRUE) -- does raw actually appear as altExp? ===\n")
sce_zk_raw <- readH5AD(h5ad, reader = "R", raw = TRUE)
cat("altExpNames with raw=TRUE:", paste(SingleCellExperiment::altExpNames(sce_zk_raw), collapse=", "), "\n")
if ("raw" %in% SingleCellExperiment::altExpNames(sce_zk_raw)) {
  raw_alt <- SingleCellExperiment::altExp(sce_zk_raw, "raw")
  cat("raw altExp dim (should be 33538 x 1222, the FULL gene raw snapshot):", paste(dim(raw_alt), collapse=" x "), "\n")
}
