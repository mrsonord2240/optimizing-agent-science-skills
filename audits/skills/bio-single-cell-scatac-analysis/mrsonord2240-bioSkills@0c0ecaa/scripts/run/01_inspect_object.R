# Purpose: Inspect the synthetic Signac object before executing the documented workflows.
# Inputs:   argv[1] = .rds object.
# Usage:    r.sh 01_inspect_object.R obj_qc.rds
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({ library(Seurat); library(Signac) })
obj <- readRDS(commandArgs(trailingOnly = TRUE)[1])
cat('cells=', ncol(obj), ' features=', nrow(obj), '\n', sep = '')
cat('assays=', paste(Assays(obj), collapse = ','), '\n', sep = '')
cat('ident_levels=', paste(levels(Idents(obj)), collapse = ','), '\n', sep = '')
cat('metadata=', paste(colnames(obj@meta.data), collapse = ','), '\n', sep = '')
