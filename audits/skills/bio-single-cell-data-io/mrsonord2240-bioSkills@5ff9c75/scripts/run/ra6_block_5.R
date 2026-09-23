library(Seurat)
library(zellkonverter)

sce <- as.SingleCellExperiment(seurat_obj)   # counts -> counts, data -> logcounts, reductions -> reducedDims
writeH5AD(sce, 'out.h5ad')
