# go-enrichment Input 4 (Variant B, regression of pre-fix Input 4): GO-DAG redundancy --
# simplify() per ontology, ont='ALL', groupGO. Blocks b03 and b05 verbatim, then simplify()
# on the ont='ALL' object directly. Tests fix claim #2: the Skill now says simplify() on
# ont='ALL' silently keeps only the first ontology (BP) rather than erroring.
suppressPackageStartupMessages({library(clusterProfiler); library(org.Hs.eg.db)})
GG <- 'F:/OpenScience/audits/bio-pathway-go-enrichment'
tab <- read.csv(file.path(GG, 'data', 'proteomics_da_table.csv'), colClasses = 'character')
tab$hit_signal <- tab$hit_signal == 'TRUE'
gene_list <- unique(tab$entrez[tab$hit_signal])
universe_ids <- unique(tab$entrez)

ego_bp <- enrichGO(gene_list, universe = universe_ids, OrgDb = org.Hs.eg.db, keyType = 'ENTREZID', ont = 'BP', readable = TRUE)
n_before <- nrow(as.data.frame(ego_bp))
ego_bp_simplified <- simplify(ego_bp, cutoff = 0.7, by = 'p.adjust', select_fun = min, measure = 'Wang')
n_after <- nrow(as.data.frame(ego_bp_simplified))
cat('simplify() single-ontology BP: terms', n_before, '->', n_after, '\n')

ego_all <- enrichGO(gene_list, universe = universe_ids, OrgDb = org.Hs.eg.db, keyType = 'ENTREZID', ont = 'ALL', readable = TRUE)
d_all <- as.data.frame(ego_all)
cat('ont=ALL: total terms', nrow(d_all), '| by ontology:', paste(names(table(d_all$ONTOLOGY)), table(d_all$ONTOLOGY), sep='=', collapse=', '), '\n')

res <- tryCatch({
  simp_all <- simplify(ego_all, cutoff = 0.7, by = 'p.adjust', select_fun = min, measure = 'Wang')
  d_simp <- as.data.frame(simp_all)
  list(status = 'no error/warning', n = nrow(d_simp), ont = unique(d_simp$ONTOLOGY))
}, warning = function(w) list(status = paste('WARNING:', conditionMessage(w))),
   error = function(e) list(status = paste('ERROR:', conditionMessage(e))))
cat('simplify(ont=ALL object) result:', res$status, '\n')
if (!is.null(res$n)) cat('  terms returned:', res$n, '| ontologies present in output:', paste(res$ont, collapse=','), '\n')
cat('SKILL.md claim: "no error and no warning - simplify() silently returns only the first',
    'ontology\'s terms (BP) and drops MF/CC entirely" -- matches:',
    isTRUE(res$status == 'no error/warning' && identical(res$ont, 'BP') && res$n == n_after), '\n')

ggo <- groupGO(gene_list, OrgDb = org.Hs.eg.db, keyType = 'ENTREZID', ont = 'BP', level = 3, readable = TRUE)
d_ggo <- as.data.frame(ggo)
cat('groupGO rows:', nrow(d_ggo), '| has p-value column:', 'pvalue' %in% colnames(d_ggo), '\n')
