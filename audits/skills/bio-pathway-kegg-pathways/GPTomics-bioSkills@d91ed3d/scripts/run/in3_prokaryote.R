# Input 3 (Edge): "This is a Pseudomonas... " -- adapted to E. coli, real KEGG-covered organism:
# "This is an E. coli RNA-seq DE list with locus-tag gene IDs. Run KEGG enrichment with the right
# organism code and keyType, without forcing an OrgDb or bitr."
suppressMessages(library(clusterProfiler))

de <- read.csv('../data/SYNTHETIC_eco_de_results.csv')
sig <- de$locus_tag[de$padj < 0.05 & de$log2FoldChange > 1]
universe <- de$locus_tag[!is.na(de$pvalue)]
cat("sig locus tags:", length(sig), " universe:", length(universe), "\n")
cat("sample sig IDs:", paste(head(sig,3), collapse=", "), "\n")

kk <- enrichKEGG(gene=sig, organism='eco', keyType='kegg',
                 universe=universe, pvalueCutoff=0.05, pAdjustMethod='BH',
                 minGSSize=5, maxGSSize=500, qvalueCutoff=0.2)
res <- as.data.frame(kk)
cat("Enriched pathways:", nrow(res), "\n")
print(head(res[order(res$p.adjust), c("ID","Description","GeneRatio","BgRatio","p.adjust","Count")], 5), row.names=FALSE)
cat("\nPlanted eco00010 (glycolysis) found:", "eco00010" %in% res$ID, "\n")

# confirm setReadable correctly errors/no-ops without an OrgDb for a prokaryote (documented failure mode)
sr_result <- tryCatch({ setReadable(kk, OrgDb=NULL) }, error=function(e) paste("ERROR:", conditionMessage(e)))
cat("\nsetReadable(kk, OrgDb=NULL) on prokaryote result:", if(is.character(sr_result)) sr_result else "no error (unexpected)", "\n")
