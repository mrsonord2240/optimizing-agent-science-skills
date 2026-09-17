# Input 7 (Adversarial, regression of pre-fix Input 7): "Just run KEGG enrichment on my
# significant genes, I don't have a background set handy." -- tests whether omitting universe
# still produces the documented tissue-specificity inflation artifact (unchanged code), AND
# whether the fixed SKILL.md's new Agent Workflow step 3 ("If no measured/background gene set is
# available, tell the user before proceeding") is now present as an explicit agent-facing
# instruction, closing pre-fix P1 finding #2.
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

cat("\n--- SKILL.md text check: is the refuse/warn instruction now an explicit Agent Workflow step? ---\n")
skill_text <- paste(readLines('../run/skill_copy/SKILL.md'), collapse="\n")
has_step <- grepl("If no measured/background gene set is available, tell the user before proceeding", skill_text, fixed=TRUE)
cat("Explicit refuse/warn step present in Agent Workflow:", has_step, "\n")
