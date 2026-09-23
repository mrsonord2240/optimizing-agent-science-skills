args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 2)
suppressPackageStartupMessages({ library(Seurat); library(Signac) })
obj <- readRDS(args[[1]])
DefaultAssay(obj) <- "peaks"
Idents(obj) <- "cell_type"
stopifnot(all(c("Tcell", "Bcell") %in% levels(Idents(obj))))
da <- FindMarkers(obj, ident.1 = "Tcell", ident.2 = "Bcell", test.use = "LR",
                  latent.vars = "nCount_peaks", logfc.threshold = 0,
                  min.pct = 0)
stopifnot(is.data.frame(da), nrow(da) == nrow(obj),
          all(c("p_val", "p_val_adj") %in% colnames(da)),
          all(is.finite(da$p_val)), all(da$p_val >= 0 & da$p_val <= 1))
write.csv(da, args[[2]], row.names = TRUE)
cat(sprintf("depth_aware_da_clean_exit rows=%d LR_latent=nCount_peaks\\n", nrow(da)))
