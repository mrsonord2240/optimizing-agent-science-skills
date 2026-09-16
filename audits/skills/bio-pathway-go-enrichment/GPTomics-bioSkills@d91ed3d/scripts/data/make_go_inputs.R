# SYNTHETIC proteomics gene lists for the go-enrichment audit (2026-09-15). NOT REAL EXPERIMENTAL DATA.
# Gene identities and GO annotations are real (org.Hs.eg.db); which genes are "quantified" and "hits" is simulated.
# universe: 3500 genes sampled from genes annotated to abundant compartments (cytosol GO:0005829, mitochondrial matrix
#   GO:0005759, nucleolus GO:0005730, ribosome GO:0005840) -- mimics the abundance bias of a DDA proteome.
# hits_signal: 40 cytoplasmic-translation genes (GO:0002181) in the universe + 110 random universe genes.
# hits_null: 150 random universe genes (no biology).
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
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
