args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 2)
suppressPackageStartupMessages({ library(Seurat); library(Signac) })
obj <- readRDS(args[[1]])
stopifnot(ncol(obj) == 270L, nrow(obj) == 222L, "nCount_peaks" %in% colnames(obj[[]]))
DefaultAssay(obj) <- "peaks"
obj <- RunTFIDF(obj)
obj <- FindTopFeatures(obj, min.cutoff = "q0")
set.seed(1)
obj <- RunSVD(obj, n = 30, verbose = FALSE)
emb <- Embeddings(obj, "lsi")
depth <- obj$nCount_peaks
cors <- apply(emb, 2, function(x) cor(x, depth, use = "complete.obs"))
drop <- which(abs(cors) > 0.5)
use <- setdiff(seq_len(min(30L, ncol(emb))), drop)
stopifnot(length(drop) >= 1L, length(use) >= 2L, all(abs(cors[drop]) > 0.5))
obj <- FindNeighbors(obj, reduction = "lsi", dims = use, verbose = FALSE)
obj <- FindClusters(obj, resolution = 0.3, verbose = FALSE)
saveRDS(obj, args[[2]])
write.csv(data.frame(component = names(cors), depth_correlation = cors,
                     dropped = seq_along(cors) %in% drop),
          sub("\\.rds$", "_depth_correlations.csv", args[[2]]), row.names = FALSE)
cat(sprintf("core_lsi_clean_exit cells=%d features=%d dropped=%s retained=%d\\n",
            ncol(obj), nrow(obj), paste(drop, collapse = ","), length(use)))
