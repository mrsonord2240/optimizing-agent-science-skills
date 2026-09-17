# Input 8 (new, auditor-authored / redundancy-pass + column-accuracy check): "Using only
# SKILL.md's Understanding Results table, what columns will my enrichPathway and gsePathway
# results actually have?" Verifies SKILL.md's post-redundancy-pass "Understanding Results"
# table (absorbed from usage-guide.md during the fix) lists the REAL column names of the
# result objects, not just claims from the old usage-guide.md copy.
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

ora_cols_claimed <- c("ID","Description","GeneRatio","BgRatio","RichFactor","FoldEnrichment",
                      "zScore","pvalue","p.adjust","qvalue","geneID","Count")
ora_cols_actual <- colnames(as.data.frame(ora))
cat("enrichResult claimed columns (SKILL.md Understanding Results):\n  ", paste(ora_cols_claimed, collapse=", "), "\n")
cat("enrichResult actual columns (this installed version):\n  ", paste(ora_cols_actual, collapse=", "), "\n")
cat("All claimed columns present in actual:", all(ora_cols_claimed %in% ora_cols_actual), "\n")
cat("Any actual columns NOT documented:", paste(setdiff(ora_cols_actual, ora_cols_claimed), collapse=", "), "\n")

ranked <- read.csv("../data/ranked_genes.csv", stringsAsFactors = FALSE)
mapped <- bitr(ranked$SYMBOL, fromType = "SYMBOL", toType = "ENTREZID", OrgDb = org.Hs.eg.db)
ranked <- merge(ranked, mapped, by.x = "SYMBOL", by.y = "SYMBOL")
gene_list <- ranked$stat
names(gene_list) <- ranked$ENTREZID
gene_list <- sort(gene_list, decreasing = TRUE)
set.seed(123)
gse <- gsePathway(geneList = gene_list, organism = "human", pvalueCutoff = 0.05, pAdjustMethod = "BH", verbose = FALSE)

gse_cols_claimed_added <- c("setSize","enrichmentScore","NES","rank","leading_edge","core_enrichment")
gse_cols_actual <- colnames(as.data.frame(gse))
cat("\ngseaResult claimed ADDED columns (SKILL.md):\n  ", paste(gse_cols_claimed_added, collapse=", "), "\n")
cat("gseaResult actual columns:\n  ", paste(gse_cols_actual, collapse=", "), "\n")
cat("All claimed added columns present:", all(gse_cols_claimed_added %in% gse_cols_actual), "\n")
