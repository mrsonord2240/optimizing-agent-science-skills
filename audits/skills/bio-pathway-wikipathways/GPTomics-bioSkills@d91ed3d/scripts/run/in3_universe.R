# Input 3 (Edge): boundary check on the SKILL's own documented claim -- "Default universe inflates
# significance" (Common Errors table + Per-Method Failure Modes). Compare universe=NULL (documented
# default, biased "all-WP-genes" background) against universe=tested-genes on a NULL gene list (no
# planted signal at all, drawn purely from the background pool) and on the planted signal list.
suppressMessages({
  library(clusterProfiler)
  library(org.Hs.eg.db)
})

de_results <- read.csv('../data/de_results_synthetic.csv', stringsAsFactors = FALSE)
all_entrez <- bitr(de_results$gene_symbol, fromType='SYMBOL', toType='ENTREZID', OrgDb=org.Hs.eg.db)$ENTREZID

set.seed(7)
# a "null" gene list: 60 random background genes with NO planted pathway membership and no
# systematic biology -- should not enrich for anything under a matched universe
bg_only <- de_results[de_results$planted_group == 'background', ]
null_symbols <- sample(bg_only$gene_symbol, 150)
null_sig <- bitr(null_symbols, fromType='SYMBOL', toType='ENTREZID', OrgDb=org.Hs.eg.db)$ENTREZID
cat("null list n:", length(null_sig), "\n")

wp_matched <- enrichWP(gene = null_sig, organism = 'Homo sapiens', universe = all_entrez,
                        pvalueCutoff = 0.05, pAdjustMethod = 'BH', minGSSize = 10, maxGSSize = 500)
wp_default <- enrichWP(gene = null_sig, organism = 'Homo sapiens', universe = NULL,
                        pvalueCutoff = 0.05, pAdjustMethod = 'BH', minGSSize = 10, maxGSSize = 500)

res_matched <- if (is.null(wp_matched)) data.frame() else as.data.frame(wp_matched)
res_default <- if (is.null(wp_default)) data.frame() else as.data.frame(wp_default)
cat("\n--- NULL gene list (background size, matched universe = length(all_entrez) =", length(all_entrez), ") ---\n")
cat("matched universe: significant terms:", nrow(res_matched), if (is.null(wp_matched)) "(enrichWP returned NULL -- no WP gene set had >=10 members among the null list)" else "", "\n")
cat("default universe=NULL: significant terms:", nrow(res_default), "\n")
if (nrow(res_default) > 0) print(res_default[order(res_default$p.adjust), c('ID','Description','p.adjust','Count')], row.names=FALSE)

# same comparison on the real planted signal list, to show N (universe size) differs even when both find real signal
sig_symbols <- de_results[de_results$padj < 0.05 & abs(de_results$log2FoldChange) > 1, 'gene_symbol']
sig <- bitr(sig_symbols, fromType='SYMBOL', toType='ENTREZID', OrgDb=org.Hs.eg.db)$ENTREZID
wp_sig_matched <- enrichWP(gene = sig, organism = 'Homo sapiens', universe = all_entrez, pvalueCutoff = 1, qvalueCutoff = 1)
wp_sig_default <- enrichWP(gene = sig, organism = 'Homo sapiens', universe = NULL, pvalueCutoff = 1, qvalueCutoff = 1)
r1 <- as.data.frame(wp_sig_matched); r2 <- as.data.frame(wp_sig_default)
cat("\n--- Planted-signal list, unfiltered (pvalueCutoff=1) to compare p.adjust magnitude for WP554 ---\n")
cat("matched universe WP554 p.adjust:", r1$p.adjust[r1$ID=='WP554'], " BgRatio:", r1$BgRatio[r1$ID=='WP554'], "\n")
cat("default universe(NULL) WP554 p.adjust:", r2$p.adjust[r2$ID=='WP554'], " BgRatio:", r2$BgRatio[r2$ID=='WP554'], "\n")
