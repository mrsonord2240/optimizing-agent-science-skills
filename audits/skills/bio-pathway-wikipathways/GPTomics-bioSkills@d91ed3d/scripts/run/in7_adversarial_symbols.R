# Input 7 (Adversarial): "Just run enrichWP directly on my significant gene symbols, don't bother
# converting IDs, I want the fastest result." -- deliberately skips bitr to test the SKILL's own
# documented failure mode ("Symbols or Ensembl into an Entrez GMT" -> "empty or near-empty result,
# NO error").
suppressMessages(library(clusterProfiler))

de_results <- read.csv('../data/de_results_synthetic.csv', stringsAsFactors = FALSE)
sig_symbols <- de_results[de_results$padj < 0.05 & abs(de_results$log2FoldChange) > 1, 'gene_symbol']
all_symbols <- de_results$gene_symbol
cat("n significant SYMBOLs (not converted to Entrez):", length(sig_symbols), "\n")

wp_wrong <- enrichWP(gene = sig_symbols, organism = 'Homo sapiens', universe = all_symbols,
                      pvalueCutoff = 0.05, pAdjustMethod = 'BH', minGSSize = 10, maxGSSize = 500)

if (is.null(wp_wrong)) {
  cat("enrichWP on raw SYMBOLs returned NULL -- matches the documented failure mode (empty result, no error)\n")
} else {
  res <- as.data.frame(wp_wrong)
  cat("n terms:", nrow(res), "(documented expectation: 0 or near-0, no error)\n")
  if (nrow(res) > 0) print(res[, c('ID','Description','Count')])
}
cat("An error/crash did NOT occur (confirms 'no error' claim):\n")
