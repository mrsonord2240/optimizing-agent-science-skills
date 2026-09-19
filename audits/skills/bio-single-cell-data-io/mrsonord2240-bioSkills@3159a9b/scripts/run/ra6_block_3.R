# Preferred R-native read of an h5ad written in Python (no reticulate)
library(anndataR)
adata <- read_h5ad('data.h5ad')
seurat_obj <- adata$to_Seurat()
# Or via Bioconductor with a pinned Python anndata:
# library(zellkonverter); sce <- readH5AD('data.h5ad'); writeH5AD(sce, 'out.h5ad')
