# Input 6 (Scope boundary): "I ran enrichKEGG on my Ensembl/SYMBOL gene list directly (no ID
# conversion) and also tried use_internal_data=TRUE for reproducibility -- something feels off,
# can you check?"
# Tests two of the Skill's own documented failure-mode claims:
#  (a) ENSEMBL/SYMBOL fed straight to enrichKEGG -> zero hits silently, no error
#  (b) use_internal_data=TRUE does NOT pin current KEGG (loads deprecated 2012 KEGG.db)
suppressMessages({
  library(clusterProfiler)
  library(org.Hs.eg.db)
})

de <- read.csv('../data/SYNTHETIC_de_results.csv')
sig_symbols <- de$gene[de$padj < 0.05 & abs(de$log2FoldChange) > 1]
universe_symbols <- de$gene[!is.na(de$pvalue)]

## (a) SYMBOL passed directly, no bitr -- documented as "zero hits, no error"
kk_wrong <- tryCatch(
  enrichKEGG(gene=sig_symbols, organism='hsa', keyType='ncbi-geneid',
             universe=universe_symbols, pvalueCutoff=0.05),
  error = function(e) paste("ERROR:", conditionMessage(e))
)
if (is.character(kk_wrong)) {
  cat("(a) enrichKEGG with raw SYMBOL IDs -> ERROR (not the documented 'silent zero hits'):", kk_wrong, "\n")
} else {
  n <- nrow(as.data.frame(kk_wrong))
  cat("(a) enrichKEGG with raw SYMBOL IDs (keyType=ncbi-geneid) -> enriched pathways:", n,
      "-- matches documented 'zero hits silently':", n==0, "\n")
}

## also try keyType='kegg' with SYMBOL (another plausible misuse)
kk_wrong2 <- tryCatch(
  enrichKEGG(gene=sig_symbols, organism='hsa', keyType='kegg',
             universe=universe_symbols, pvalueCutoff=0.05),
  error = function(e) paste("ERROR:", conditionMessage(e))
)
if (is.character(kk_wrong2)) {
  cat("(a2) enrichKEGG SYMBOL with keyType='kegg' -> ERROR:", kk_wrong2, "\n")
} else {
  n2 <- nrow(as.data.frame(kk_wrong2))
  cat("(a2) enrichKEGG SYMBOL with keyType='kegg' -> enriched pathways:", n2, "\n")
}

## (b) use_internal_data=TRUE
sig_entrez <- suppressMessages(bitr(sig_symbols, 'SYMBOL', 'ENTREZID', org.Hs.eg.db))$ENTREZID
universe   <- suppressMessages(bitr(universe_symbols, 'SYMBOL', 'ENTREZID', org.Hs.eg.db))$ENTREZID
kk_internal <- tryCatch(
  enrichKEGG(gene=sig_entrez, organism='hsa', keyType='ncbi-geneid',
             universe=universe, pvalueCutoff=0.05, use_internal_data=TRUE),
  error = function(e) paste("ERROR:", conditionMessage(e))
)
if (is.character(kk_internal)) {
  cat("\n(b) use_internal_data=TRUE -> ERROR (matches 'stale/absent' documented symptom):", kk_internal, "\n")
} else {
  n3 <- nrow(as.data.frame(kk_internal))
  cat("\n(b) use_internal_data=TRUE -> ran, pathways:", n3, "(this branch worked; compare vs live below)\n")
}
