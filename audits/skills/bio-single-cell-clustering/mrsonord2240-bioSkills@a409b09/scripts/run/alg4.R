.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages(library(Seurat))
data('pbmc_small', package='SeuratObject')
o <- pbmc_small
o <- FindNeighbors(o, dims=1:10, verbose=FALSE)
r <- try(FindClusters(o, resolution=0.6, algorithm=4, verbose=FALSE), silent=TRUE)
cat(as.character(r), '\n')
