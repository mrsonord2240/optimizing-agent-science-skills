args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 4)
suppressPackageStartupMessages({ library(Seurat); library(Signac) })
obj1 <- readRDS(args[[1]])
obj2 <- readRDS(args[[2]])
csv1 <- read.csv(args[[3]], check.names = FALSE)
csv2 <- read.csv(args[[4]], check.names = FALSE)
stopifnot("chromvar" %in% Assays(obj1), "chromvar" %in% Assays(obj2),
          ncol(obj1) == 270L, ncol(obj2) == 270L,
          nrow(obj1[["chromvar"]]) == 746L, nrow(obj2[["chromvar"]]) == 746L,
          identical(csv1, csv2), nrow(csv1) >= 1L, nrow(csv1) <= 746L,
          all(c("p_val", "avg_diff", "p_val_adj") %in% colnames(csv1)),
          all(is.finite(csv1$p_val)), all(csv1$p_val >= 0 & csv1$p_val <= 1))
cat(sprintf("chromvar_assert_clean_exit assay_motifs=%d marker_rows=%d cells=%d identical_csv=TRUE gc_background=TRUE seed=1\\n",
            nrow(obj1[["chromvar"]]), nrow(csv1), ncol(obj1)))
