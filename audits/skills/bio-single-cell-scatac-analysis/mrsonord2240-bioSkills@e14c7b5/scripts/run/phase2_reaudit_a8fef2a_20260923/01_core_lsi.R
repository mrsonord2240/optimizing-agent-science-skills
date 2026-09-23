# Purpose: Fresh regression of the documented Signac TF-IDF/LSI workflow and depth diagnosis.
# Usage: rs.sh 01_core_lsi.R obj_qc.rds core_lsi.rds
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({ library(Seurat); library(Signac) })
a <- commandArgs(trailingOnly = TRUE); stopifnot(length(a) == 2)
obj <- readRDS(a[1]); DefaultAssay(obj) <- 'peaks'
stopifnot(ncol(obj) == 270L, nrow(obj[['peaks']]) == 222L)
obj <- RunTFIDF(obj)
obj <- FindTopFeatures(obj, min.cutoff = 'q0')
set.seed(1)
obj <- RunSVD(obj)
emb <- Embeddings(obj, 'lsi')
cors <- apply(emb, 2, function(x) cor(x, obj$nCount_peaks))
drop <- which(abs(cors) > 0.5)
use <- setdiff(seq_len(min(30L, ncol(emb))), drop)
cat('depth_cor_first10=', paste(format(cors[seq_len(10L)], digits=4), collapse=','),
    ' selected_drop=', paste(drop, collapse=','), '\n', sep='')
stopifnot(ncol(emb) >= 30L, length(drop) >= 1L, length(use) >= 2L, all(is.finite(cors)))
obj <- FindNeighbors(obj, reduction = 'lsi', dims = use, verbose = FALSE)
obj <- FindClusters(obj, algorithm = 3, resolution = 0.5, verbose = FALSE)
saveRDS(obj, a[2])
cat('cells=', ncol(obj), ' peaks=', nrow(obj[['peaks']]), ' lsi_dims=', ncol(emb),
    ' drop=', paste(drop, collapse = ','), ' retained=', length(use),
    ' clusters=', length(unique(Idents(obj))), '\n', sep='')
