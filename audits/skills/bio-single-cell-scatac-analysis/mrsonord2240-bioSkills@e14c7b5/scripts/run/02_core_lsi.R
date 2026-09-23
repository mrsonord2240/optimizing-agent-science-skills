# Purpose: Execute the documented Signac TF-IDF/LSI and per-component depth diagnosis.
# Inputs:   argv[1] = input .rds; argv[2] = output .rds.
# Usage:    r.sh 02_core_lsi.R obj_qc.rds core_lsi.rds
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({ library(Seurat); library(Signac) })
a <- commandArgs(trailingOnly = TRUE); stopifnot(length(a) == 2)
obj <- readRDS(a[1])
DefaultAssay(obj) <- 'peaks'
obj <- RunTFIDF(obj)
obj <- FindTopFeatures(obj, min.cutoff = 'q0')
obj <- RunSVD(obj)
emb <- Embeddings(obj, 'lsi')
cors <- apply(emb, 2, function(x) cor(x, obj$nCount_peaks))
drop <- which(abs(cors) > 0.5)
use <- setdiff(seq_len(min(30, ncol(emb))), drop)
stopifnot(length(use) >= 2, all(is.finite(cors)))
obj <- FindNeighbors(obj, reduction = 'lsi', dims = use, verbose = FALSE)
obj <- FindClusters(obj, algorithm = 3, resolution = 0.5, verbose = FALSE)
saveRDS(obj, a[2])
cat('lsi_dims=', ncol(emb), ' drop=', paste(drop, collapse=','), ' use=', paste(use, collapse=','), ' clusters=', length(unique(Idents(obj))), '\n', sep='')
