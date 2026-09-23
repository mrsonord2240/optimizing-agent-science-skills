# Phase-2 Input 2: real filtered 10x PBMC H5 load with Seurat v5.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
library(Seurat)
path <- 'F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/public-data/pbmc_1k_v3_filtered_feature_bc_matrix.h5'
counts <- Read10X_h5(path)
seu <- CreateSeuratObject(counts = counts, project = 'phase2_io', min.cells = 3, min.features = 200)
mat <- LayerData(seu, layer = 'counts')
cat('counts_dim genes_x_cells', nrow(mat), ncol(mat), '\n')
cat('sparse', inherits(mat, 'sparseMatrix'), '\n')
stopifnot(nrow(mat) == 15246, ncol(mat) == 1176, inherits(mat, 'sparseMatrix'))
cat('PASS input2\n')
