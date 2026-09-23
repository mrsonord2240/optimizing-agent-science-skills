# New input beyond the fixer's verification: (a) check the anndataR R>=4.5
# caveat is accurate in this environment, and (b) regression-check Input 7
# from the original audit (SeuratDisk Convert() to h5ad should still fail on
# Seurat v5) is unaffected by this fix, using a freshly built Seurat object.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))

cat("=== anndataR R-version caveat check ===\n")
cat("R version:", as.character(getRversion()), "\n")
cat("Is R >= 4.5?", getRversion() >= "4.5", "\n")
cat("anndataR installed?", requireNamespace("anndataR", quietly = TRUE), "\n")
cat("(SKILL.md's caveat: anndataR requires R>=4.5, falls back to zellkonverter/schard on R 4.4)\n")

cat("\n=== Regression: SeuratDisk still broken on Seurat v5 (Input 7 baseline, untouched by this fix) ===\n")
library(Seurat)
library(SeuratDisk)
set.seed(1)
h5file <- "F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/public-data/pbmc_1k_v3_filtered_feature_bc_matrix.h5"
counts <- Read10X_h5(h5file)
seu <- CreateSeuratObject(counts = counts, min.cells = 3, min.features = 200)
tmp_h5s <- "F:/OpenScience/audits/bio-single-cell-data-io/data/ra4_seuratdisk_test.h5Seurat"
res <- tryCatch({
  SaveH5Seurat(seu, filename = tmp_h5s, overwrite = TRUE)
  Convert(tmp_h5s, dest = "h5ad", overwrite = TRUE)
  "SUCCEEDED (unexpected -- would contradict SKILL.md)"
}, error = function(e) paste("FAILED as expected:", conditionMessage(e)))
cat("SeuratDisk Convert result:", res, "\n")
