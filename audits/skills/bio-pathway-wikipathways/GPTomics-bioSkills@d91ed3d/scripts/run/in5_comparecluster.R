# Input 5 (Stress / multi-part): "Run enrichment against WikiPathways for both my up- and
# down-regulated genes and show me which pathways are specific to each direction" -- the
# compareCluster(fun='enrichWP') pattern from the Decision Tree table.
suppressMessages({
  library(clusterProfiler)
  library(org.Hs.eg.db)
})

de_results <- read.csv('../data/de_results_synthetic.csv', stringsAsFactors = FALSE)
up_symbols   <- de_results[de_results$padj < 0.05 & de_results$log2FoldChange > 1, 'gene_symbol']
down_symbols <- de_results[de_results$padj < 0.05 & de_results$log2FoldChange < -1, 'gene_symbol']
cat("n up:", length(up_symbols), " n down:", length(down_symbols), "\n")

up <- bitr(up_symbols, fromType='SYMBOL', toType='ENTREZID', OrgDb=org.Hs.eg.db)$ENTREZID
down <- bitr(down_symbols, fromType='SYMBOL', toType='ENTREZID', OrgDb=org.Hs.eg.db)$ENTREZID
all_entrez <- bitr(de_results$gene_symbol, fromType='SYMBOL', toType='ENTREZID', OrgDb=org.Hs.eg.db)$ENTREZID

t0 <- Sys.time()
cc <- compareCluster(geneClusters = list(up = up, down = down), fun = 'enrichWP',
                      organism = 'Homo sapiens', universe = all_entrez,
                      pvalueCutoff = 0.05, pAdjustMethod = 'BH', minGSSize = 10, maxGSSize = 500)
cat("compareCluster took", as.numeric(Sys.time()-t0, units='secs'), "s\n")

res <- as.data.frame(cc)
cat("n rows:", nrow(res), "\n")
print(res[order(res$Cluster, res$p.adjust), c('Cluster','ID','Description','p.adjust','Count')], row.names=FALSE)

up_terms <- unique(res$ID[res$Cluster=='up'])
down_terms <- unique(res$ID[res$Cluster=='down'])
cat("\nWP554 (planted UP) assigned to up cluster only:", 'WP554' %in% up_terms && !('WP554' %in% down_terms), "\n")
cat("WP430 (planted DOWN) assigned to down cluster only:", 'WP430' %in% down_terms && !('WP430' %in% up_terms), "\n")
cat("terms unique to up:", length(setdiff(up_terms, down_terms)), " unique to down:", length(setdiff(down_terms, up_terms)), " shared:", length(intersect(up_terms, down_terms)), "\n")
