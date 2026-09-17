# SYNTHETIC proteomics gene lists for the go-enrichment re-audit (2026-09-16), post-fix.
# NOT REAL EXPERIMENTAL DATA. Gene identities and GO annotations are real (org.Hs.eg.db); which
# genes are "quantified" and "hits" is simulated. Same design as the pre-fix audit's data (a
# planted GO:0002181 cytoplasmic-translation signal in a DDA-abundance-biased universe) so scores
# from this run are comparable to the pre-fix report.
suppressPackageStartupMessages({library(org.Hs.eg.db); library(AnnotationDbi)})
set.seed(915)
cc <- AnnotationDbi::select(org.Hs.eg.db, keys = c('GO:0005829', 'GO:0005759', 'GO:0005730', 'GO:0005840'), keytype = 'GOALL', columns = 'ENTREZID')
pool <- unique(cc$ENTREZID)
universe <- sample(pool, 3500)
trans <- unique(AnnotationDbi::select(org.Hs.eg.db, keys = 'GO:0002181', keytype = 'GOALL', columns = 'ENTREZID')$ENTREZID)
tin <- intersect(trans, universe)
sig <- c(sample(tin, min(40, length(tin))), sample(setdiff(universe, trans), 110))
null <- sample(universe, 150)
sym <- function(x) AnnotationDbi::mapIds(org.Hs.eg.db, x, 'SYMBOL', 'ENTREZID')
uni <- AnnotationDbi::mapIds(org.Hs.eg.db, universe, 'UNIPROT', 'ENTREZID', multiVals = 'first')
tab <- data.frame(entrez = universe, symbol = sym(universe), uniprot = uni, stringsAsFactors = FALSE)
tab$hit_signal <- tab$entrez %in% sig; tab$hit_null <- tab$entrez %in% null
set.seed(1); tab$log2FC <- ifelse(tab$hit_signal, sample(c(-1, 1), nrow(tab), TRUE) * runif(nrow(tab), 1, 2), rnorm(nrow(tab), 0, 0.3))
tab$adj.P.Val <- ifelse(tab$hit_signal, runif(nrow(tab), 1e-6, 0.04), runif(nrow(tab), 0.06, 1))
write.csv(tab, 'F:/OpenScience/audits/bio-pathway-go-enrichment/data/proteomics_da_table.csv', row.names = FALSE)
cat('universe', length(universe), '| translation genes in universe', length(tin), '| signal hits', length(sig), '| uniprot NA', sum(is.na(uni)), '\n')
cat('org.Hs.eg.db', as.character(packageVersion('org.Hs.eg.db')), '| GO.db', as.character(packageVersion('GO.db')), '| clusterProfiler', as.character(packageVersion('clusterProfiler')), '\n')
