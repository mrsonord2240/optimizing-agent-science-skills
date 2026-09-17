# Input 1 (Canonical): "I have 97 significant genes (symbols) from a DESeq2 contrast and a
# measured background of 3000 genes. Convert to Entrez, run Reactome over-representation, and
# give me the top pathways with fold enrichment, deduplicated so I'm not double-counting
# parent/child pathways." -- follows SKILL.md's enrichPathway pattern verbatim.
suppressMessages({
  library(ReactomePA)
  library(clusterProfiler)
  library(org.Hs.eg.db)
})

sig_symbols <- read.csv("../data/significant_genes.csv", stringsAsFactors = FALSE)$SYMBOL
bg_symbols  <- read.csv("../data/background_genes.csv", stringsAsFactors = FALSE)$SYMBOL

sig_entrez <- bitr(sig_symbols, fromType = "SYMBOL", toType = "ENTREZID", OrgDb = org.Hs.eg.db)$ENTREZID
universe   <- bitr(bg_symbols,  fromType = "SYMBOL", toType = "ENTREZID", OrgDb = org.Hs.eg.db)$ENTREZID

ora <- enrichPathway(gene = sig_entrez, organism = "human", universe = universe,
                     pvalueCutoff = 0.05, qvalueCutoff = 0.2,
                     minGSSize = 10, maxGSSize = 500, readable = TRUE)

df <- as.data.frame(ora)
cat("Rows returned:", nrow(df), "\n")
cat("Top 5 by p.adjust:\n")
print(df[1:min(5, nrow(df)), c("ID", "Description", "GeneRatio", "BgRatio", "FoldEnrichment", "p.adjust", "Count")])

cat("\nIs planted pathway R-HSA-877300 (Interferon gamma signaling) recovered? ",
    "R-HSA-877300" %in% df$ID, "\n")
if ("R-HSA-877300" %in% df$ID) {
  row <- df[df$ID == "R-HSA-877300", ]
  cat("Rank:", which(df$ID == "R-HSA-877300"), "of", nrow(df),
      "| p.adjust:", row$p.adjust, "| FoldEnrichment:", row$FoldEnrichment, "\n")
}

write.csv(df, "out1_ora_results.csv", row.names = FALSE)
