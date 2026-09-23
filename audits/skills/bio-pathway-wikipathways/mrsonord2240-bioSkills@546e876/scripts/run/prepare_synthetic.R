suppressPackageStartupMessages({
  library(rWikiPathways)
  library(org.Hs.eg.db)
  library(AnnotationDbi)
})
args <- commandArgs(trailingOnly = TRUE)
run_dir <- args[[1]]
dir.create(run_dir, recursive = TRUE, showWarnings = FALSE)
sig_entrez <- unique(as.character(getXrefList('WP554', 'L')))
all_ids <- unique(c(sig_entrez, head(keys(org.Hs.eg.db, keytype = 'ENTREZID'), 600)))
mapped <- AnnotationDbi::select(org.Hs.eg.db, keys = all_ids, keytype = 'ENTREZID', columns = 'SYMBOL')
mapped <- mapped[!is.na(mapped$SYMBOL) & !duplicated(mapped$SYMBOL), c('ENTREZID', 'SYMBOL')]
sig_symbols <- mapped$SYMBOL[mapped$ENTREZID %in% sig_entrez]
stopifnot(length(sig_symbols) >= 10)
de <- data.frame(
  gene_symbol = mapped$SYMBOL,
  log2FoldChange = ifelse(mapped$SYMBOL %in% sig_symbols, 3, seq(-1.5, 1.5, length.out = nrow(mapped))),
  pvalue = ifelse(mapped$SYMBOL %in% sig_symbols, 1e-8, 0.5),
  padj = ifelse(mapped$SYMBOL %in% sig_symbols, 1e-6, 0.8)
)
write.csv(de, file.path(run_dir, 'de_results.csv'), row.names = FALSE)
writeLines(sig_entrez, file.path(run_dir, 'sig_entrez.txt'))
writeLines(mapped$ENTREZID, file.path(run_dir, 'universe_entrez.txt'))
cat(sprintf('SYNTHETIC rows=%d sig_symbols=%d sig_entrez=%d\n', nrow(de), length(sig_symbols), length(sig_entrez)))
