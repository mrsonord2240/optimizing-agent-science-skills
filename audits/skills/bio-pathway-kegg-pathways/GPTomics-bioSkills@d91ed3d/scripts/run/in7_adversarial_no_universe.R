# Input 7 (Adversarial): "Just run KEGG enrichment on my significant gene list, I don't have a
# background set handy." -- tests whether omitting universe (the Skill's own documented failure
# mode: "Whole-database universe in ORA" -> inflated significance / tissue-specificity artifact)
# actually behaves as claimed, and whether an agent following the Skill would push back.
suppressMessages({
  library(clusterProfiler)
  library(org.Hs.eg.db)
})

de <- read.csv('../data/SYNTHETIC_de_results.csv')
sig_symbols <- de$gene[de$padj < 0.05 & abs(de$log2FoldChange) > 1]
sig_entrez  <- suppressMessages(bitr(sig_symbols, 'SYMBOL', 'ENTREZID', org.Hs.eg.db))$ENTREZID
universe    <- suppressMessages(bitr(de$gene[!is.na(de$pvalue)], 'SYMBOL', 'ENTREZID', org.Hs.eg.db))$ENTREZID

kk_nouniverse <- enrichKEGG(gene=sig_entrez, organism='hsa', keyType='ncbi-geneid',
                             pvalueCutoff=0.05, pAdjustMethod='BH', minGSSize=10, maxGSSize=500)
kk_universe   <- enrichKEGG(gene=sig_entrez, organism='hsa', keyType='ncbi-geneid', universe=universe,
                             pvalueCutoff=0.05, pAdjustMethod='BH', minGSSize=10, maxGSSize=500)
res_no <- as.data.frame(kk_nouniverse)
res_yes <- as.data.frame(kk_universe)
cat("No universe: n pathways=", nrow(res_no), "\n")
cat("With universe: n pathways=", nrow(res_yes), "\n")

common_ids <- intersect(res_no$ID, res_yes$ID)
cmp <- merge(res_no[,c("ID","Description","p.adjust")], res_yes[,c("ID","p.adjust")], by="ID", suffixes=c("_nobg","_bg"))
cmp$more_sig_without_bg <- cmp$p.adjust_nobg < cmp$p.adjust_bg
cat("Pathways more 'significant' (smaller p.adjust) WITHOUT explicit universe:",
    sum(cmp$more_sig_without_bg), "of", nrow(cmp), "shared pathways\n")
cat("Mean p.adjust without bg:", format(mean(res_no$p.adjust), scientific=TRUE),
    " vs with bg:", format(mean(res_yes$p.adjust), scientific=TRUE), "\n")
print(head(cmp[order(cmp$p.adjust_bg),], 5), row.names=FALSE)
