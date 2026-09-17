# go-enrichment Input 1 (Canonical, regression of pre-fix audit's Input 1):
# GO BP ORA on a proteomics DA hit list with the quantified proteome as universe.
# SKILL.md "Run the GO ORA" block (b01), post-fix, executed VERBATIM.
# Data: SYNTHETIC hit/universe assignment over REAL org.Hs.eg.db annotations
# (data/make_go_inputs.R); planted signal is GO:0002181 cytoplasmic translation.
suppressPackageStartupMessages({library(clusterProfiler); library(org.Hs.eg.db)})
GG <- 'F:/OpenScience/audits/bio-pathway-go-enrichment'
tab <- read.csv(file.path(GG, 'data', 'proteomics_da_table.csv'), colClasses = 'character')
tab$hit_signal <- tab$hit_signal == 'TRUE'
gene_list <- unique(tab$entrez[tab$hit_signal])          # foreground: the DA hits
universe_ids <- unique(tab$entrez)                       # universe: every quantified protein
cat('foreground', length(gene_list), '| universe', length(universe_ids), '\n')
blk <- list.files(file.path(GG, 'runs', 'blocks'), pattern = '^b01', full.names = TRUE)
t0 <- Sys.time()
res <- tryCatch({ sys.source(blk, envir = globalenv()); 'OK' }, error = function(e) paste('ERROR:', conditionMessage(e)))
cat('[enrichGO block verbatim]', res, '| elapsed s:', round(as.numeric(difftime(Sys.time(), t0, units = 'secs')), 1), '\n')
d <- as.data.frame(ego)
cat('terms returned:', nrow(d), '| columns:', paste(colnames(d), collapse = ','), '\n')
# Claim under test (fix log #1): enrichResult now documented as including RichFactor,
# FoldEnrichment, zScore, matching the actually-returned columns.
expected_cols <- c('ID','Description','GeneRatio','BgRatio','RichFactor','FoldEnrichment','zScore','pvalue','p.adjust','qvalue','geneID','Count')
cat('columns match SKILL.md documented list exactly:', identical(colnames(d), expected_cols), '\n')
if (nrow(d)) {
  # independent manual computation, cross-checked against the FoldEnrichment column
  fe_manual <- sapply(strsplit(d$GeneRatio, '/'), function(x) as.numeric(x[1]) / as.numeric(x[2])) /
               sapply(strsplit(d$BgRatio, '/'), function(x) as.numeric(x[1]) / as.numeric(x[2]))
  cat('FoldEnrichment column matches manual (k/n)/(M/N) (max abs diff):', max(abs(d$FoldEnrichment - fe_manual)), '\n')
  rf_manual <- sapply(strsplit(d$GeneRatio, '/'), function(x) as.numeric(x[1])) /
               sapply(strsplit(d$BgRatio, '/'), function(x) as.numeric(x[1]))
  cat('RichFactor column matches manual k/M (max abs diff):', max(abs(d$RichFactor - rf_manual)), '\n')
  print(head(d[, c('ID', 'Description', 'GeneRatio', 'BgRatio', 'RichFactor', 'FoldEnrichment', 'zScore', 'p.adjust', 'Count')], 8))
  cat('planted term GO:0002181 present:', 'GO:0002181' %in% d$ID, '| rank by p.adjust:', match('GO:0002181', d$ID[order(d$p.adjust)]), '\n')
  cat('N (universe genes with BP annotation) from BgRatio:', unique(sapply(strsplit(d$BgRatio, '/'), `[`, 2)), '\n')
  cat('readable Description (not raw IDs):', !all(grepl('^GO:', d$Description)), '\n')
  write.csv(d, file.path(GG, 'runs', 'in1_terms.csv'), row.names = FALSE)
}
