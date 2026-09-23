# Phase-2 Input 7: adversarial request for the obsolete SeuratDisk route.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
library(Seurat)
library(SeuratDisk)
src <- 'F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/public-data/pbmc_1k_v3_filtered_feature_bc_matrix.h5'
file <- 'F:/OpenScience/audits/bio-single-cell-data-io/data/fp2_seuratdisk.h5Seurat'
seu <- CreateSeuratObject(Read10X_h5(src), min.cells=3, min.features=200)
result <- tryCatch({ SaveH5Seurat(seu, filename=file, overwrite=TRUE); Convert(file, dest='h5ad', overwrite=TRUE); 'SUCCEEDED' }, error=function(e) paste('FAILED', conditionMessage(e)))
cat('SeuratDisk_result', result, '\n')
stopifnot(startsWith(result, 'FAILED'))
cat('PASS input7\n')
