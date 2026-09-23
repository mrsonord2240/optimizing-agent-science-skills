# Phase-2 Input 4: use the skill's Seurat -> SCE -> h5ad route and persist scale.data separately.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
Sys.setenv(BASILISK_EXTERNAL_DIR = 'F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/cache/basilisk')
library(Seurat)
library(zellkonverter)
src <- 'F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/public-data/pbmc_1k_v3_filtered_feature_bc_matrix.h5'
out <- 'F:/OpenScience/audits/bio-single-cell-data-io/data/fp2_from_seurat.h5ad'
sidecar <- 'F:/OpenScience/audits/bio-single-cell-data-io/data/fp2_scale_data.rds'
set.seed(13)
seu <- CreateSeuratObject(Read10X_h5(src), min.cells=3, min.features=200)
seu <- NormalizeData(seu, verbose=FALSE)
seu <- FindVariableFeatures(seu, nfeatures=500, verbose=FALSE)
seu <- ScaleData(seu, verbose=FALSE)
seu <- RunPCA(seu, npcs=10, verbose=FALSE)
seu <- RunUMAP(seu, dims=1:10, verbose=FALSE)
scale_data <- as.matrix(LayerData(seu, layer='scale.data'))
saveRDS(scale_data, sidecar)
stopifnot(is.matrix(readRDS(sidecar)), isTRUE(all.equal(scale_data, readRDS(sidecar))))
sce <- as.SingleCellExperiment(seu)
writeH5AD(sce, out)
cat('seurat_layers', paste(Layers(seu), collapse=','), 'sce_assays', paste(SummarizedExperiment::assayNames(sce), collapse=','), 'reductions', paste(SingleCellExperiment::reducedDimNames(sce), collapse=','), '\n')
cat('scale_sidecar_dim', paste(dim(scale_data), collapse='x'), '\n')
cat('PASS input4_R\n')
