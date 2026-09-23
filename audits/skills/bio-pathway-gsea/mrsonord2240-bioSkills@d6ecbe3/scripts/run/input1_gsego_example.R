source("F:/OpenScience/wt/pathway-gsea/pathway-analysis/gsea/examples/gsea_go.R", echo = FALSE)
out <- file.path(tempdir(), "gsea_go_results.csv")
stopifnot(file.exists(out))
tab <- read.csv(out, check.names = FALSE)
stopifnot(nrow(tab) > 0, all(c("NES", "p.adjust", "core_enrichment") %in% names(tab)))
hit <- tab[tab$ID == "GO:0006260", , drop = FALSE]
stopifnot(nrow(hit) == 1, hit$NES > 0, hit$p.adjust < 0.05)
cat(sprintf("ASSERT input1 rows=%d GO0006260_NES=%.6f padj=%.3g\n", nrow(tab), hit$NES, hit$p.adjust))
