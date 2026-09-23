library(schard)
sce_raw <- schard::h5ad2sce('data.h5ad', use.raw = TRUE)   # full-gene raw snapshot
sce_hvg <- schard::h5ad2sce('data.h5ad', use.raw = FALSE)  # default: X as stored (e.g. HVG-subsetted)
length(SingleCellExperiment::altExpNames(sce_hvg))          # runnable "diff slot inventories" check for zellkonverter's raw=TRUE -- 0 means it silently failed
