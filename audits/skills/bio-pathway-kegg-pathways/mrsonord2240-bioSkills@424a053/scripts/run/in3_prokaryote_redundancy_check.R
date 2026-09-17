# Input 3 (Edge + REDUNDANCY-PASS CHECK, new): "This is an E. coli RNA-seq DE list with locus-tag
# gene IDs. Run KEGG enrichment with the right organism code and keyType, without forcing an OrgDb
# or bitr."
#
# This input doubles as one of the two required NEW checks: the fix log's redundancy pass moved
# usage-guide.md's "Common Organism Codes" table into SKILL.md verbatim. An agent that had only
# SKILL.md loaded (not usage-guide.md -- the normal case, since usage-guide.md is optional
# supplementary material) must still be able to look up that 'eco' = E. coli K-12, locus tags,
# no OrgDb -- entirely from SKILL.md. This script uses ONLY the organism-code fact as stated in
# the FIXED SKILL.md (verified by reading it directly, reproduced in the comment below) with no
# reference to usage-guide.md at all, to confirm the moved content is both present and correct.
#
# SKILL.md "Common Organism Codes" table (fixed version) states:
#   | eco | E. coli K-12 | Bacterial; locus tags (b-numbers) |
# and "Decision Tree by Scenario" states:
#   Bacterial / prokaryotic data -> locus tags, keyType='kegg', NO OrgDb/bitr
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

sr_result <- tryCatch({ setReadable(kk, OrgDb=NULL) }, error=function(e) paste("ERROR:", conditionMessage(e)))
cat("\nsetReadable(kk, OrgDb=NULL) on prokaryote result:", if(is.character(sr_result)) sr_result else "no error (unexpected)", "\n")
