# Input 4 (Variant B): "I have a human DE list with log2 fold-changes and a universe. Run SPIA so
# direction and network position are used, tell me which signaling pathways are activated vs
# inhibited, and explain why this is not appropriate for metabolic pathways."
suppressMessages({
  library(SPIA)
  library(clusterProfiler)
  library(org.Hs.eg.db)
})

de <- read.csv('../data/SYNTHETIC_de_results.csv')
sig <- de[de$padj < 0.05, ]
map <- suppressMessages(bitr(sig$gene, 'SYMBOL', 'ENTREZID', org.Hs.eg.db))
de_vec <- setNames(sig$log2FoldChange[match(map$SYMBOL, sig$gene)], map$ENTREZID)
de_vec <- de_vec[!duplicated(names(de_vec))]
universe <- suppressMessages(bitr(de$gene[!is.na(de$pvalue)], 'SYMBOL', 'ENTREZID', org.Hs.eg.db))$ENTREZID

cat("DE vec length:", length(de_vec), " universe:", length(universe), "\n")
pct_missing <- 100 * mean(!(names(de_vec) %in% universe))
cat("pct of de IDs missing from universe:", round(pct_missing,3), "%\n")

t0 <- Sys.time()
res <- spia(de=de_vec, all=universe, organism='hsa', nB=200, plots=FALSE, verbose=FALSE)
cat("SPIA wall time:", round(as.numeric(Sys.time()-t0,units="secs"),1), "s\n")
cat("Pathways scored:", nrow(res), "\n")
sig_spia <- res[res$pGFdr < 0.05, c("Name","ID","pSize","NDE","pNDE","tA","pPERT","pG","pGFdr","Status")]
print(head(sig_spia[order(sig_spia$pGFdr),], 10), row.names=FALSE)

row_cc <- res[res$ID=="04110",]
cat("\nPlanted hsa04110 (Cell cycle) row: pGFdr=", if(nrow(row_cc)>0) signif(row_cc$pGFdr,3) else "NOT SCORED",
    " Status=", if(nrow(row_cc)>0) row_cc$Status else "NA", " tA=", if(nrow(row_cc)>0) round(row_cc$tA,2) else "NA", "\n")
row_ins <- res[res$ID=="04910",]
cat("Planted hsa04910 (Insulin signaling) row: pGFdr=", if(nrow(row_ins)>0) signif(row_ins$pGFdr,3) else "NOT SCORED",
    " Status=", if(nrow(row_ins)>0) row_ins$Status else "NA", " tA=", if(nrow(row_ins)>0) round(row_ins$tA,2) else "NA", "\n")

# metabolic-map claim check: is hsa00010 (glycolysis, metabolic) even present/scored by SPIA at all?
row_gly <- res[res$ID=="00010",]
cat("\nMetabolic hsa00010 (Glycolysis) present in SPIA output at all:", nrow(row_gly)>0, "\n")
write.csv(res, "in4_spia_full.csv", row.names=FALSE)
