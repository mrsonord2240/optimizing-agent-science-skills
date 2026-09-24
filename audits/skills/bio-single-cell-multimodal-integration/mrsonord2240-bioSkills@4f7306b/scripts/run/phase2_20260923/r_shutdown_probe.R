.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages(library(Seurat))
cat('R_SHUTDOWN_PROBE loaded Seurat ', as.character(packageVersion('Seurat')), '\n', sep = '')
gc()
