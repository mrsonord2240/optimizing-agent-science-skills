# go-enrichment Input 4 (variant): redundant ancestor lineages. SKILL.md blocks b03 (simplify per ontology) and b04 (ont='ALL'
# plus groupGO) run verbatim, then simplify() called on the ont='ALL' object -- the failure mode the Skill documents.
# Data: SYNTHETIC hit assignment over REAL org.Hs.eg.db annotations.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({library(clusterProfiler); library(org.Hs.eg.db)})
GG <- 'F:/OpenScience/audits/bio-pathway-go-enrichment'
tab <- read.csv(file.path(GG, 'data', 'proteomics_da_table.csv'), colClasses = 'character')
gene_list <- unique(tab$entrez[tab$hit_signal == 'TRUE']); universe_ids <- unique(tab$entrez)
b03 <- list.files(file.path(GG, 'runs', 'blocks'), pattern = '^b03', full.names = TRUE)
b05 <- list.files(file.path(GG, 'runs', 'blocks'), pattern = '^b05', full.names = TRUE)
t0 <- Sys.time()
r3 <- tryCatch({ sys.source(b03, envir = globalenv()); 'OK' }, error = function(e) paste('ERROR:', conditionMessage(e)))
cat('[simplify block verbatim]', r3, '| elapsed s:', round(as.numeric(difftime(Sys.time(), t0, units = 'secs')), 1), '\n')
ego_bp_raw <- enrichGO(gene_list, universe = universe_ids, OrgDb = org.Hs.eg.db, keyType = 'ENTREZID', ont = 'BP', readable = TRUE)
cat('BP terms before simplify:', nrow(as.data.frame(ego_bp_raw)), '| after simplify:', nrow(as.data.frame(ego_bp)), '\n')
kept <- as.data.frame(ego_bp); raw <- as.data.frame(ego_bp_raw)
cat('translation-lineage terms before:', sum(grepl('translation', raw$Description, ignore.case = TRUE)),
    '| after:', sum(grepl('translation', kept$Description, ignore.case = TRUE)), '\n')
t0 <- Sys.time()
r4 <- tryCatch({ sys.source(b05, envir = globalenv()); 'OK' }, error = function(e) paste('ERROR:', conditionMessage(e)))
cat('[ont=ALL + groupGO block verbatim]', r4, '| elapsed s:', round(as.numeric(difftime(Sys.time(), t0, units = 'secs')), 1), '\n')
da <- as.data.frame(ego_all)
cat('ont=ALL terms:', nrow(da), '| ONTOLOGY column present:', 'ONTOLOGY' %in% colnames(da), '| per ontology:', paste(names(table(da$ONTOLOGY)), table(da$ONTOLOGY)), '\n')
gg <- as.data.frame(ggo); cat('groupGO rows:', nrow(gg), '| has p-value column:', any(grepl('pvalue|p.adjust', colnames(gg))), '\n')
bad <- tryCatch({ s <- simplify(ego_all, cutoff = 0.7, by = 'p.adjust', select_fun = min, measure = 'Wang'); paste('returned', nrow(as.data.frame(s)), 'terms (was', nrow(da), ')') },
                error = function(e) paste('ERROR:', conditionMessage(e)))
cat('simplify() on the ont=ALL object ->', bad, '\n')
