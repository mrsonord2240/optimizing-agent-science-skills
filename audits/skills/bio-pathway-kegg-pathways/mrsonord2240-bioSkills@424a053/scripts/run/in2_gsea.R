# Input 2 (Variant A, regression of pre-fix Input 2): "Run GSEA against KEGG on my full ranked
# gene list (no cutoff) and tell me which pathways come up on the up- vs down-regulated side."
# Unchanged code path (GSEA section byte-identical to pre-fix SKILL.md except the set.seed comment
# wording) -- rerun to confirm parity.
suppressMessages({
  library(clusterProfiler)
  library(org.Hs.eg.db)
})

de <- read.csv('../data/SYNTHETIC_de_results.csv')

geneList <- de$log2FoldChange; names(geneList) <- de$entrez
geneList <- sort(geneList[!is.na(geneList)], decreasing=TRUE)
cat("Ranked vector length:", length(geneList), " names are entrez, decreasing:", !is.unsorted(rev(geneList)), "\n")

set.seed(123)
kk2 <- gseKEGG(geneList=geneList, organism='hsa', keyType='ncbi-geneid',
               minGSSize=10, maxGSSize=500, pvalueCutoff=0.05, seed=TRUE)
res <- as.data.frame(kk2)
cat("Total GSEA-significant KEGG sets:", nrow(res), "\n")
top <- head(res[order(res$p.adjust), c("ID","Description","NES","p.adjust")], 8)
print(top, row.names=FALSE)

up_row   <- res[res$ID=="hsa04110",]
down_row <- res[res$ID=="hsa04910",]
cat("\nPlanted UP hsa04110 found:", nrow(up_row)>0, if(nrow(up_row)>0) paste("NES=",round(up_row$NES,2),"p.adjust=",signif(up_row$p.adjust,3)) else "", "\n")
cat("Planted DOWN hsa04910 found:", nrow(down_row)>0, if(nrow(down_row)>0) paste("NES=",round(down_row$NES,2),"p.adjust=",signif(down_row$p.adjust,3)) else "", "\n")
write.csv(res, "in2_gsea_full.csv", row.names=FALSE)
