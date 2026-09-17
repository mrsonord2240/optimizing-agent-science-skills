suppressMessages({
  library(clusterProfiler); library(enrichplot); library(org.Hs.eg.db); library(ggplot2)
})
d <- readRDS("../data/gene_data.rds")
ego <- enrichGO(gene = d$entrez, OrgDb = org.Hs.eg.db, ont = 'BP',
                 pvalueCutoff = 0.05, qvalueCutoff = 0.2, readable = TRUE)
# Force down to exactly 1 significant term to test the true near-empty edge case.
ego@result <- ego@result[1, , drop = FALSE]
cat("n terms forced to:", nrow(ego@result), "\n")
r <- tryCatch({ ts <- pairwise_termsim(ego); emapplot(ts); "emapplot SUCCEEDED with 1 term" },
              error = function(e) paste("emapplot ERROR with 1 term:", conditionMessage(e)))
cat(r, "\n")
