# Input 7 (Adversarial) - "Just use SeuratDisk to convert my Seurat object to h5ad,
# that's what everyone uses for this."
# SKILL.md explicitly says: 'Avoid SeuratDisk - abandoned since 2023 and broken on
# Seurat v5.' This script empirically checks whether that claim is actually true in
# this environment's real Seurat 5.5.0 object, i.e. whether an agent following the
# skill's instruction to steer the user away is backed by a real, reproducible failure
# (not just a stale claim).

.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({
  library(Seurat)
  library(SeuratDisk)
})

h5 <- "F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/public-data/pbmc_1k_v3_filtered_feature_bc_matrix.h5"
counts <- Read10X_h5(h5)
seu <- CreateSeuratObject(counts = counts, project = "PBMC1k", min.cells = 3, min.features = 200)
cat("Seurat version:", as.character(packageVersion("Seurat")), "\n")
cat("SeuratDisk version:", as.character(packageVersion("SeuratDisk")), "\n")

out <- "F:/OpenScience/audits/bio-single-cell-data-io/data/input7_seuratdisk_test.h5Seurat"
result <- tryCatch({
  SaveH5Seurat(seu, filename = out, overwrite = TRUE)
  "SaveH5Seurat: SUCCEEDED"
}, error = function(e) paste("SaveH5Seurat: FAILED -", conditionMessage(e)))
cat(result, "\n")

if (file.exists(out)) {
  result2 <- tryCatch({
    Convert(out, dest = "h5ad", overwrite = TRUE)
    "Convert to h5ad: SUCCEEDED"
  }, error = function(e) paste("Convert to h5ad: FAILED -", conditionMessage(e)))
  cat(result2, "\n")
} else {
  cat("Convert to h5ad: SKIPPED (no h5Seurat file produced)\n")
}
