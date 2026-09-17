# Input 2 (Variant A / GSEA): "I have a full ranked vector of test statistics for all 3000
# measured genes. Build the named ENTREZ vector, fix the seed, run Reactome GSEA, and show me
# the leading-edge genes for the top pathway." -- follows SKILL.md's gsePathway pattern.
suppressMessages({
  library(ReactomePA)
  library(clusterProfiler)
  library(org.Hs.eg.db)
})

ranked <- read.csv("../data/ranked_genes.csv", stringsAsFactors = FALSE)
mapped <- bitr(ranked$SYMBOL, fromType = "SYMBOL", toType = "ENTREZID", OrgDb = org.Hs.eg.db)
ranked <- merge(ranked, mapped, by.x = "SYMBOL", by.y = "SYMBOL")

gene_list <- ranked$stat
names(gene_list) <- ranked$ENTREZID
gene_list <- sort(gene_list, decreasing = TRUE)

set.seed(123)
gse <- gsePathway(geneList = gene_list, organism = "human",
                  pvalueCutoff = 0.05, pAdjustMethod = "BH", verbose = FALSE)

df <- as.data.frame(gse)
cat("Rows returned:", nrow(df), "\n")
cat("Top 5 by p.adjust:\n")
print(df[1:min(5, nrow(df)), c("ID", "Description", "setSize", "NES", "p.adjust")])

cat("\nIs planted pathway R-HSA-877300 recovered?", "R-HSA-877300" %in% df$ID, "\n")
if ("R-HSA-877300" %in% df$ID) {
  row <- df[df$ID == "R-HSA-877300", ]
  cat("Rank:", which(df$ID == "R-HSA-877300"), "of", nrow(df),
      "| NES:", row$NES, "| p.adjust:", row$p.adjust, "\n")
  le <- strsplit(row$core_enrichment, "/")[[1]]
  cat("Leading edge core_enrichment count:", length(le), "\n")
}

write.csv(df, "out2_gsea_results.csv", row.names = FALSE)
