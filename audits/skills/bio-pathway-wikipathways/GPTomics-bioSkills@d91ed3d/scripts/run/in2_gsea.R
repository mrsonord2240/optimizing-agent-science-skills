# Input 2 (Variant A): usage-guide.md "ORA vs GSEA" prompt -- full ranked DE result, no cutoff,
# gseWP per the SKILL.md GSEA section pattern (named decreasing Entrez vector, set.seed(123)).
suppressMessages({
  library(clusterProfiler)
  library(org.Hs.eg.db)
})

de_results <- read.csv('../data/de_results_synthetic.csv', stringsAsFactors = FALSE)

gsea_map <- bitr(de_results$gene_symbol, fromType = 'SYMBOL', toType = 'ENTREZID', OrgDb = org.Hs.eg.db)
gl <- setNames(de_results$log2FoldChange[match(gsea_map$SYMBOL, de_results$gene_symbol)], gsea_map$ENTREZID)
gl <- sort(gl[!duplicated(names(gl))], decreasing = TRUE)
cat("ranked vector length:", length(gl), "\n")
cat("names(gl) is character:", is.character(names(gl)), " sorted decreasing:", !is.unsorted(rev(gl)), "\n")

set.seed(123)
t0 <- Sys.time()
wp_gsea <- gseWP(geneList = gl, organism = 'Homo sapiens',
                  pvalueCutoff = 0.05, pAdjustMethod = 'BH', minGSSize = 10, maxGSSize = 500)
cat("gseWP took", as.numeric(Sys.time() - t0, units = 'secs'), "s\n")

res <- as.data.frame(wp_gsea)
cat("n significant terms:", nrow(res), "\n")
print(res[order(res$p.adjust), c('ID','Description','NES','p.adjust')], row.names = FALSE)

cat("\nWP554 present:", 'WP554' %in% res$ID, "\n")
if ('WP554' %in% res$ID) cat("WP554 NES:", res$NES[res$ID=='WP554'], " p.adjust:", res$p.adjust[res$ID=='WP554'], "\n")
cat("WP430 present:", 'WP430' %in% res$ID, "\n")
if ('WP430' %in% res$ID) cat("WP430 NES:", res$NES[res$ID=='WP430'], " p.adjust:", res$p.adjust[res$ID=='WP430'], "\n")

# determinism check: re-run with the same seed
set.seed(123)
wp_gsea2 <- gseWP(geneList = gl, organism = 'Homo sapiens',
                   pvalueCutoff = 0.05, pAdjustMethod = 'BH', minGSSize = 10, maxGSSize = 500)
res2 <- as.data.frame(wp_gsea2)
same_ids <- identical(sort(res$ID), sort(res2$ID))
same_nes <- if (same_ids) all.equal(res[order(res$ID),'NES'], res2[order(res2$ID),'NES']) else "N/A (different ID sets)"
cat("\nRe-run with same seed -> identical term set:", same_ids, "; NES match:", isTRUE(same_nes), "\n")
