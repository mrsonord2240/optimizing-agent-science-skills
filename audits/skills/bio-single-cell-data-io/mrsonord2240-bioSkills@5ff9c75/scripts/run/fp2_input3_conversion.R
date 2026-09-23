# Phase-2 Input 3: AnnData to SCE conversion, including the documented raw-recovery route.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
Sys.setenv(BASILISK_EXTERNAL_DIR = 'F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/cache/basilisk')
library(zellkonverter)
library(SingleCellExperiment)
library(schard)
path <- 'F:/OpenScience/audits/bio-single-cell-data-io/data/fp2_rich.h5ad'
sce_zk <- readH5AD(path, reader = 'R', raw = TRUE)
sce_raw <- schard::h5ad2sce(path, use.raw = TRUE)
sce_hvg <- schard::h5ad2sce(path, use.raw = FALSE)
cat('zell_dim', paste(dim(sce_zk), collapse='x'), 'zell_altExp_length', length(altExpNames(sce_zk)), 'zell_assays', paste(assayNames(sce_zk), collapse=','), '\n')
cat('schard_raw_dim', paste(dim(sce_raw), collapse='x'), 'schard_hvg_dim', paste(dim(sce_hvg), collapse='x'), '\n')
cat('schard_raw_nonzero', any(assay(sce_raw, 'X') != 0), 'schard_raw_has_na', any(is.na(assay(sce_raw, 'X')@x)), '\n')
stopifnot(identical(dim(sce_zk), c(700L, 1222L)), length(altExpNames(sce_zk)) == 0L,
          identical(dim(sce_raw), c(33538L, 1222L)), identical(dim(sce_hvg), c(700L, 1222L)),
          any(assay(sce_raw, 'X') != 0), !any(is.na(assay(sce_raw, 'X')@x)))
cat('PASS input3\n')
