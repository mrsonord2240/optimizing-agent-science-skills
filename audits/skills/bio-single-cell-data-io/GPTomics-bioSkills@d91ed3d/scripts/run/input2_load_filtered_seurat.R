# Input 2 (Variant A) - "Load the filtered 10X PBMC h5 into Seurat and tell me
# how many cells and genes it has."
# Follows SKILL.md pattern: Read10X_h5() -> CreateSeuratObject(min.cells=3, min.features=200)

.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
library(Seurat)

h5 <- "F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/public-data/pbmc_1k_v3_filtered_feature_bc_matrix.h5"

counts <- Read10X_h5(h5)
cat("class(counts):", class(counts), "\n")
cat("Raw matrix dim (genes x cells):", paste(dim(counts), collapse=" x "), "\n")

seurat_obj <- CreateSeuratObject(counts = counts, project = "PBMC1k", min.cells = 3, min.features = 200)
print(seurat_obj)
cat("Cells:", ncol(seurat_obj), "\n")
cat("Genes:", nrow(seurat_obj), "\n")
cat("Seurat version:", as.character(packageVersion("Seurat")), "\n")
