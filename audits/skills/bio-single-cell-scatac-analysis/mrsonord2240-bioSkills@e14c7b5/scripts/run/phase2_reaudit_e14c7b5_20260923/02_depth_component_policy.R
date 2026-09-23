args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 1)
suppressPackageStartupMessages({ library(Seurat); library(Signac) })
obj <- readRDS(args[[1]])
emb <- Embeddings(obj, "lsi")
cors <- apply(emb, 2, function(x) cor(x, obj$nCount_peaks, use = "complete.obs"))
dropped <- which(abs(cors) > 0.5)
retained <- setdiff(seq_len(min(30L, ncol(emb))), dropped)
stopifnot(length(dropped) >= 1L, length(retained) >= 2L,
          all(abs(cors[dropped]) > 0.5), all(abs(cors[retained]) <= 0.5))
cat(sprintf("depth_policy_clean_exit dropped=%s retained=%s\\n",
            paste(dropped, collapse = ","), paste(retained, collapse = ",")))
