# Input 1 (Canonical): "I have 240ish significant genes from a DESeq2 contrast as SYMBOLs and the
# rest of the expressed genes as background. Convert both to Entrez, run KEGG pathway ORA for human
# with the measured universe, and give me the top pathways by adjusted p-value with fold enrichment."
suppressMessages({
  library(clusterProfiler)
  library(org.Hs.eg.db)
})

de <- read.csv('../data/SYNTHETIC_de_results.csv')

sig_symbols <- de$gene[de$padj < 0.05 & abs(de$log2FoldChange) > 1]
sig_entrez  <- suppressMessages(bitr(sig_symbols, fromType='SYMBOL', toType='ENTREZID', OrgDb=org.Hs.eg.db))$ENTREZID
universe    <- suppressMessages(bitr(de$gene[!is.na(de$pvalue)], fromType='SYMBOL', toType='ENTREZID', OrgDb=org.Hs.eg.db))$ENTREZID

cat("sig genes:", length(sig_symbols), "-> entrez:", length(sig_entrez),
    "(conversion loss", round(100*(1-length(sig_entrez)/length(sig_symbols)),1), "%)\n")
cat("universe:", length(universe), "\n")

kk <- enrichKEGG(gene=sig_entrez, organism='hsa', keyType='ncbi-geneid',
                 universe=universe, pvalueCutoff=0.05, pAdjustMethod='BH',
                 minGSSize=10, maxGSSize=500, qvalueCutoff=0.2)
kk <- setReadable(kk, OrgDb=org.Hs.eg.db, keyType='ENTREZID')
res <- as.data.frame(kk)
cat("\nTotal enriched pathways:", nrow(res), "\n")
res$FoldEnrichment <- sapply(strsplit(res$GeneRatio,"/"), function(x) as.numeric(x[1])/as.numeric(x[2])) /
                        sapply(strsplit(res$BgRatio,"/"), function(x) as.numeric(x[1])/as.numeric(x[2]))
top <- head(res[order(res$p.adjust), c("ID","Description","GeneRatio","BgRatio","p.adjust","qvalue","Count","FoldEnrichment")], 10)
print(top, row.names=FALSE)

cat("\nPlanted pathway hsa04110 present?", "hsa04110" %in% res$ID, "\n")
if ("hsa04110" %in% res$ID) {
  row <- res[res$ID=="hsa04110",]
  cat("hsa04110 rank by p.adjust:", which(res$ID[order(res$p.adjust)]=="hsa04110"), "of", nrow(res), "\n")
  cat("hsa04110 p.adjust:", row$p.adjust, " Count:", row$Count, " GeneRatio:", row$GeneRatio, "\n")
}
write.csv(res, "in1_kegg_ora_full.csv", row.names=FALSE)
