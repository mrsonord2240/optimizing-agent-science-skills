suppressPackageStartupMessages({library(clusterProfiler); library(org.Hs.eg.db)})
GG <- 'F:/OpenScience/audits/bio-pathway-go-enrichment'
tab <- read.csv(file.path(GG, 'data', 'proteomics_da_table.csv'), colClasses = 'character')
tab$hit_signal <- tab$hit_signal == 'TRUE'
gene_list <- unique(tab$entrez[tab$hit_signal])
universe_ids <- unique(tab$entrez)
ego_all <- enrichGO(gene_list, universe = universe_ids, OrgDb = org.Hs.eg.db, keyType = 'ENTREZID', ont = 'ALL', readable = TRUE)
simp_all <- simplify(ego_all, cutoff = 0.7, by = 'p.adjust', select_fun = min, measure = 'Wang')
d <- as.data.frame(simp_all)
print(table(d$ONTOLOGY))
print(d[, c('ONTOLOGY','ID','Description','p.adjust')])
