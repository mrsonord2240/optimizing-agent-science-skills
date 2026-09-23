.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
Sys.setenv(BASILISK_EXTERNAL_DIR = "F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/cache/basilisk")

library(Seurat)
library(zellkonverter)

set.seed(42)
h5file <- "F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/public-data/pbmc_1k_v3_filtered_feature_bc_matrix.h5"
counts <- Read10X_h5(h5file)
seu <- CreateSeuratObject(counts = counts, project = "reaudit_ra2", min.cells = 3, min.features = 200)
seu <- NormalizeData(seu)
seu <- FindVariableFeatures(seu, nfeatures = 500)
seu <- ScaleData(seu)
seu <- RunPCA(seu, npcs = 10, verbose = FALSE)
seu <- RunUMAP(seu, dims = 1:10, verbose = FALSE)  # second reduction, not tested by the fixer

cat("=== Seurat object before conversion ===\n")
cat("Layers:", Layers(seu), "\n")
cat("Reductions:", Reductions(seu), "\n")
cat("Cells x genes (counts):", ncol(seu), "x", nrow(seu), "\n")

sce <- as.SingleCellExperiment(seu)
cat("\n=== after as.SingleCellExperiment() ===\n")
cat("assayNames:", SummarizedExperiment::assayNames(sce), "\n")
cat("reducedDimNames:", SingleCellExperiment::reducedDimNames(sce), "\n")

out_h5ad <- "F:/OpenScience/audits/bio-single-cell-data-io/data/ra2_from_seurat.h5ad"
writeH5AD(sce, out_h5ad)
cat("Wrote", out_h5ad, "\n")
