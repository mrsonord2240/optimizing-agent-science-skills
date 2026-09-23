source("F:/OpenScience/wt/pathway-gsea/pathway-analysis/gsea/examples/gsea_msigdb.R", echo = FALSE)
out <- file.path(tempdir(), "gsea_hallmark_results.csv")
stopifnot(file.exists(out))
tab <- read.csv(out, check.names = FALSE)
stopifnot(nrow(tab) > 0, all(c("NES", "p.adjust") %in% names(tab)))
hit <- tab[tab$ID == "HALLMARK_OXIDATIVE_PHOSPHORYLATION", , drop = FALSE]
stopifnot(nrow(hit) == 1, hit$NES > 0, hit$p.adjust < 0.05)
cat(sprintf("ASSERT input2 rows=%d OXPHOS_NES=%.6f padj=%.3g\n", nrow(tab), hit$NES, hit$p.adjust))
