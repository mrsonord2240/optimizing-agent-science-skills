# go-enrichment Input 5 (stress): multi-part request -- up and down proteins separately, fold enrichment reported, redundancy
# collapsed, a custom gene set via enricher, and a statement of the universe. SKILL.md blocks b01/b03/b05 (enricher) used.
# Data: SYNTHETIC hit assignment over REAL org.Hs.eg.db annotations.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({library(clusterProfiler); library(org.Hs.eg.db); library(AnnotationDbi)})
GG <- 'F:/OpenScience/audits/bio-pathway-go-enrichment'
tab <- read.csv(file.path(GG, 'data', 'proteomics_da_table.csv'), stringsAsFactors = FALSE)
tab$entrez <- as.character(tab$entrez)
universe_ids <- unique(tab$entrez)
fe <- function(d) if (!nrow(d)) d else { g <- sapply(strsplit(d$GeneRatio, '/'), function(x) as.numeric(x[1]) / as.numeric(x[2]))
  b <- sapply(strsplit(d$BgRatio, '/'), function(x) as.numeric(x[1]) / as.numeric(x[2])); d$fold_enrichment <- round(g / b, 2); d }
blk <- list.files(file.path(GG, 'runs', 'blocks'), pattern = '^b01', full.names = TRUE)
for (dir in c('up', 'down')) {
  gene_list <- unique(tab$entrez[tab$hit_signal & if (dir == 'up') tab$log2FC > 0 else tab$log2FC < 0])
  cat('---', dir, 'proteins:', length(gene_list), '\n')
  r <- tryCatch({ sys.source(blk, envir = globalenv()); 'OK' }, error = function(e) paste('ERROR:', conditionMessage(e)))
  d <- fe(as.data.frame(ego))
  cat('[enrichGO verbatim]', r, '| terms:', nrow(d), '\n')
  if (nrow(d)) print(head(d[order(d$p.adjust), c('ID', 'Description', 'fold_enrichment', 'p.adjust', 'Count')], 4))
  if (nrow(d) > 1) { s <- simplify(ego, cutoff = 0.7, by = 'p.adjust', select_fun = min, measure = 'Wang')
    cat('after simplify:', nrow(as.data.frame(s)), 'terms\n') }
}
# mixed list (both directions together), for the cancellation warning the Skill makes
gene_list <- unique(tab$entrez[tab$hit_signal]); sys.source(blk, envir = globalenv())
cat('--- mixed up+down list:', length(gene_list), 'proteins ->', nrow(as.data.frame(ego)), 'terms\n')
# custom gene set (enricher): a 3-set collection built from GO annotations, as an in-house/MSigDB-style TERM2GENE
sel <- c('GO:0002181', 'GO:0006099', 'GO:0006414')
t2g <- do.call(rbind, lapply(sel, function(g) { e <- AnnotationDbi::select(org.Hs.eg.db, keys = g, keytype = 'GOALL', columns = 'ENTREZID')$ENTREZID
  data.frame(term = g, gene = unique(e), stringsAsFactors = FALSE) }))
t2g <- t2g[t2g$gene %in% universe_ids, ]
b06 <- list.files(file.path(GG, 'runs', 'blocks'), pattern = '^b06', full.names = TRUE)
r5 <- tryCatch({ sys.source(b06, envir = globalenv()); 'OK' }, error = function(e) paste('ERROR:', conditionMessage(e)))
cat('[enricher block verbatim]', r5, '| TERM2GENE rows:', nrow(t2g), '| terms:', nrow(as.data.frame(ego_custom)), '\n')
print(fe(as.data.frame(ego_custom))[, c('ID', 'GeneRatio', 'BgRatio', 'fold_enrichment', 'p.adjust')])
