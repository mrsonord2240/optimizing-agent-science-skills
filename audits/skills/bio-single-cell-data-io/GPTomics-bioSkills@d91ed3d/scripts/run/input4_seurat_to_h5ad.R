# Input 4 (Variant B) - exact Example Prompt from usage-guide.md:
# "Move this Seurat object to h5ad for Python and verify no layers were dropped"
#
# SKILL.md's conversion table lists tools by AnnData<->SCE and AnnData<->SCE<->Seurat
# (anndataR) but anndataR is not installable in this environment (R>=4.5, see TOOLS.md).
# SKILL.md gives NO explicit code pattern for Seurat -> h5ad using the other tools it
# names (zellkonverter is AnnData<->SCE only, not Seurat directly; schard is h5ad->Seurat
# read-only). This script follows the only implied route: Seurat -> SCE (Seurat's own
# as.SingleCellExperiment) -> h5ad (zellkonverter::writeH5AD) -- something the agent would
# have to infer, not something the skill states directly.

.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
Sys.setenv(BASILISK_EXTERNAL_DIR = "F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/cache/basilisk")
suppressPackageStartupMessages({
  library(Seurat)
  library(zellkonverter)
})

h5 <- "F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/public-data/pbmc_1k_v3_filtered_feature_bc_matrix.h5"
counts <- Read10X_h5(h5)
seu <- CreateSeuratObject(counts = counts, project = "PBMC1k", min.cells = 3, min.features = 200)
seu <- NormalizeData(seu, verbose = FALSE)
seu <- FindVariableFeatures(seu, nfeatures = 500, verbose = FALSE)
seu <- ScaleData(seu, verbose = FALSE)
seu <- RunPCA(seu, npcs = 10, verbose = FALSE)
seu$batch <- factor("sample1")

cat("Seurat object before conversion:\n")
print(seu)
cat("Reductions:", paste(Reductions(seu), collapse=", "), "\n")
cat("Layers in RNA assay:", paste(Layers(seu[["RNA"]]), collapse=", "), "\n")

sce <- as.SingleCellExperiment(seu)
cat("\nAfter as.SingleCellExperiment: dim (genes x cells):", paste(dim(sce), collapse=" x "), "\n")
cat("assayNames:", paste(SummarizedExperiment::assayNames(sce), collapse=", "), "\n")
cat("reducedDimNames:", paste(SingleCellExperiment::reducedDimNames(sce), collapse=", "), "\n")

out <- "F:/OpenScience/audits/bio-single-cell-data-io/data/input4_from_seurat.h5ad"
writeH5AD(sce, out)
cat("\nWrote", out, "\n")
