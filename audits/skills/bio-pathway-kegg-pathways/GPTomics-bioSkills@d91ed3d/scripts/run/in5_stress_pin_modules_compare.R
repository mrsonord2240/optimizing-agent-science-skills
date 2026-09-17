# Input 5 (Stress / multi-part): "Pin the current human KEGG release as a snapshot, record the
# date, run my ORA against the snapshot so a rerun next year gives the same pathways, also run
# KEGG module enrichment to localize which sub-process is hit, and compare KEGG enrichment between
# my up- and down-regulated gene sets in one faceted call."
suppressMessages({
  library(clusterProfiler)
  library(org.Hs.eg.db)
  library(gson)
})

de <- read.csv('../data/SYNTHETIC_de_results.csv')
sig_symbols <- de$gene[de$padj < 0.05 & abs(de$log2FoldChange) > 1]
sig_entrez  <- suppressMessages(bitr(sig_symbols, 'SYMBOL', 'ENTREZID', org.Hs.eg.db))$ENTREZID
universe    <- suppressMessages(bitr(de$gene[!is.na(de$pvalue)], 'SYMBOL', 'ENTREZID', org.Hs.eg.db))$ENTREZID

## --- 5a. pin the release ---
t0 <- Sys.time()
k <- gson_KEGG('hsa')
k@accessed_date <- as.character(Sys.Date())
snapshot <- file.path(tempdir(), 'kegg_hsa.gson')
write.gson(k, snapshot)
k2 <- read.gson(snapshot)
cat("gson_KEGG fetch+pin wall time:", round(as.numeric(Sys.time()-t0,units="secs"),1), "s\n")
cat("accessed_date survives write/read:", k2@accessed_date == as.character(Sys.Date()), "(", k2@accessed_date, ")\n")

kk_pinned <- enricher(sig_entrez, gson=k2, universe=universe, pvalueCutoff=0.05, qvalueCutoff=0.2)
res_pinned <- as.data.frame(kk_pinned)
cat("Pinned ORA pathways:", nrow(res_pinned), " planted hsa04110 present:", "hsa04110" %in% res_pinned$ID, "\n")

## --- 5b. module enrichment ---
mkk <- enrichMKEGG(gene=sig_entrez, organism='hsa', keyType='ncbi-geneid', universe=universe, pvalueCutoff=0.05)
res_m <- as.data.frame(mkk)
cat("\nModule enrichment (enrichMKEGG) hits:", nrow(res_m), "\n")
if (nrow(res_m) > 0) print(head(res_m[order(res_m$p.adjust), c("ID","Description","Count","p.adjust")], 5), row.names=FALSE)

## --- 5c. compareCluster up vs down ---
up_entrez   <- suppressMessages(bitr(de$gene[de$padj<0.05 & de$log2FoldChange>1],  'SYMBOL','ENTREZID', org.Hs.eg.db))$ENTREZID
down_entrez <- suppressMessages(bitr(de$gene[de$padj<0.05 & de$log2FoldChange< -1],'SYMBOL','ENTREZID', org.Hs.eg.db))$ENTREZID
clusters <- list(up=up_entrez, down=down_entrez)
ck <- compareCluster(geneClusters=clusters, fun='enrichKEGG', organism='hsa', keyType='ncbi-geneid', universe=universe)
res_ck <- as.data.frame(ck)
cat("\ncompareCluster rows:", nrow(res_ck), "\n")
cc_cc <- res_ck[res_ck$ID=="hsa04110" & res_ck$Cluster=="up",]
cc_ins<- res_ck[res_ck$ID=="hsa04910" & res_ck$Cluster=="down",]
cat("hsa04110 appears ONLY under 'up' cluster:",
    nrow(res_ck[res_ck$ID=="hsa04110" & res_ck$Cluster=="up",])>0,
    "&& not under down:", nrow(res_ck[res_ck$ID=="hsa04110" & res_ck$Cluster=="down",])==0, "\n")
cat("hsa04910 appears ONLY under 'down' cluster:",
    nrow(res_ck[res_ck$ID=="hsa04910" & res_ck$Cluster=="down",])>0,
    "&& not under up:", nrow(res_ck[res_ck$ID=="hsa04910" & res_ck$Cluster=="up",])==0, "\n")
write.csv(res_pinned, "in5_pinned_ora.csv", row.names=FALSE)
write.csv(res_m, "in5_modules.csv", row.names=FALSE)
write.csv(res_ck, "in5_comparecluster.csv", row.names=FALSE)
