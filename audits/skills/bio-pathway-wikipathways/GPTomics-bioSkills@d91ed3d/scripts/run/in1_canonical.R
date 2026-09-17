# Input 1 (Canonical): usage-guide.md "Basic enrichment" prompt, followed verbatim as the SKILL.md
# directs -- bitr symbols to Entrez, universe = tested genes, enrichWP, setReadable, top by p.adjust.
suppressMessages({
  library(clusterProfiler)
  library(org.Hs.eg.db)
})

de_results <- read.csv('../data/de_results_synthetic.csv', stringsAsFactors = FALSE)
sig_symbols <- de_results[de_results$padj < 0.05 & abs(de_results$log2FoldChange) > 1, 'gene_symbol']
cat("n significant symbols:", length(sig_symbols), "\n")

sig <- bitr(sig_symbols, fromType = 'SYMBOL', toType = 'ENTREZID', OrgDb = org.Hs.eg.db)$ENTREZID
all_entrez <- bitr(de_results$gene_symbol, fromType = 'SYMBOL', toType = 'ENTREZID', OrgDb = org.Hs.eg.db)$ENTREZID
cat("bitr sig conversion:", length(sig), "/", length(sig_symbols), "\n")
cat("bitr universe conversion:", length(all_entrez), "/", nrow(de_results), "\n")

t0 <- Sys.time()
wp <- enrichWP(gene = sig, organism = 'Homo sapiens', universe = all_entrez,
               pvalueCutoff = 0.05, pAdjustMethod = 'BH', minGSSize = 10, maxGSSize = 500,
               qvalueCutoff = 0.2)
cat("enrichWP took", as.numeric(Sys.time() - t0, units = 'secs'), "s\n")

wp <- setReadable(wp, OrgDb = org.Hs.eg.db, keyType = 'ENTREZID')
res <- as.data.frame(wp)
cat("n significant terms:", nrow(res), "\n")
top15 <- head(res[order(res$p.adjust), c('ID','Description','GeneRatio','BgRatio','p.adjust','qvalue','Count')], 15)
print(top15, row.names = FALSE)

cat("\nWP554 present:", 'WP554' %in% res$ID, "\n")
if ('WP554' %in% res$ID) {
  row <- res[res$ID == 'WP554', ]
  cat("WP554 rank by p.adjust:", which(order(res$p.adjust) == which(res$ID=='WP554')), "of", nrow(res), "\n")
  cat("WP554 p.adjust:", row$p.adjust, " Count:", row$Count, " GeneRatio:", row$GeneRatio, "\n")
}
