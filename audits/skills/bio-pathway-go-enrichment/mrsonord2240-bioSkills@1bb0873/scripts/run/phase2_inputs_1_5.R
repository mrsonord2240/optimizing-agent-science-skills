# Phase 2 re-audit regression runner for bio-pathway-go-enrichment.
# Runs the two shipped examples unchanged plus three source-guided ORA variants.

suppressPackageStartupMessages({
  library(clusterProfiler)
  library(org.Hs.eg.db)
})

source_root <- '/mnt/openscience/wt/pathway-go-enrichment/pathway-analysis/go-enrichment'
cat('R=', R.version.string, '\n', sep = '')
cat('clusterProfiler=', as.character(packageVersion('clusterProfiler')), '\n', sep = '')
cat('org.Hs.eg.db=', as.character(packageVersion('org.Hs.eg.db')), '\n', sep = '')

# Input 1: execute the shipped basic example without changing its code.
e1 <- new.env(parent = globalenv())
source(file.path(source_root, 'examples', 'go_enrichment_basic.R'), local = e1)
stopifnot(inherits(e1$ego_bp, 'enrichResult'))
stopifnot(all(c('GeneRatio', 'BgRatio', 'FoldEnrichment', 'p.adjust', 'Count') %in% colnames(as.data.frame(e1$ego_bp))))
cat('INPUT1_OK terms=', nrow(as.data.frame(e1$ego_bp)), '\n', sep = '')

# Input 2: execute the shipped per-ontology example unchanged.
e2 <- new.env(parent = globalenv())
source(file.path(source_root, 'examples', 'go_all_ontologies.R'), local = e2)
stopifnot(is.data.frame(e2$combined))
stopifnot(nrow(e2$combined) > 0L)
cat('INPUT2_OK combined_terms=', nrow(e2$combined), '\n', sep = '')

# Input 3: explicit-universe BP ORA; verify output contract and cutoff inspection route.
universe_ids <- head(keys(org.Hs.eg.db, keytype = 'ENTREZID'), 3000L)
gene_list <- head(universe_ids, 200L)
ora <- enrichGO(gene = gene_list, universe = universe_ids, OrgDb = org.Hs.eg.db,
                keyType = 'ENTREZID', ont = 'BP', pAdjustMethod = 'BH',
                pvalueCutoff = 1, qvalueCutoff = 1, minGSSize = 10, maxGSSize = 500,
                readable = TRUE)
ora_df <- as.data.frame(ora)
stopifnot(nrow(ora_df) > 0L)
stopifnot(all(c('FoldEnrichment', 'pvalue', 'p.adjust', 'Count') %in% colnames(ora_df)))
stopifnot(all(ora_df$p.adjust >= ora_df$pvalue | is.na(ora_df$p.adjust)))
cat('INPUT3_OK explicit_universe_terms=', nrow(ora_df), 'annotated_universe=', length(ora@universe), '\n', sep = '')

# Input 4: all-ontology simplify and non-significance groupGO boundary.
ora_all <- enrichGO(gene = gene_list, universe = universe_ids, OrgDb = org.Hs.eg.db,
                    keyType = 'ENTREZID', ont = 'ALL', pvalueCutoff = 0.05, qvalueCutoff = 0.2,
                    minGSSize = 10, maxGSSize = 500)
simple_all <- simplify(ora_all, cutoff = 0.7, by = 'p.adjust', select_fun = min, measure = 'Wang')
grouped <- groupGO(gene_list, OrgDb = org.Hs.eg.db, keyType = 'ENTREZID', ont = 'BP', level = 3)
simple_df <- as.data.frame(simple_all)
group_df <- as.data.frame(grouped)
stopifnot(nrow(simple_df) > 0L, 'ONTOLOGY' %in% colnames(simple_df))
stopifnot(!('p.adjust' %in% colnames(group_df)))
cat('INPUT4_OK simplify_terms=', nrow(simple_df), 'ontologies=', paste(sort(unique(simple_df$ONTOLOGY)), collapse = ','), 'groupGO_rows=', nrow(group_df), '\n', sep = '')

# Input 5: UniProt conversion plus a custom local TERM2GENE enrichment.
uniprot_ids <- head(keys(org.Hs.eg.db, keytype = 'UNIPROT'), 1000L)
converted <- bitr(uniprot_ids, fromType = 'UNIPROT', toType = 'ENTREZID', OrgDb = org.Hs.eg.db)
converted <- converted[!duplicated(converted$ENTREZID), ]
stopifnot(nrow(converted) >= 10L)
custom_universe <- head(unique(converted$ENTREZID), 30L)
custom_foreground <- head(custom_universe, 10L)
t2g <- rbind(data.frame(term = 'FOREGROUND_TERM', gene = custom_foreground),
             data.frame(term = 'BACKGROUND_TERM', gene = custom_universe[11:30]))
custom <- enricher(custom_foreground, TERM2GENE = t2g, universe = custom_universe,
                   pvalueCutoff = 1, qvalueCutoff = 1, minGSSize = 3, maxGSSize = 500)
custom_df <- as.data.frame(custom)
stopifnot(nrow(custom_df) >= 1L, 'FOREGROUND_TERM' %in% custom_df$ID)
cat('INPUT5_OK uniprot_mapped=', nrow(converted), 'custom_terms=', nrow(custom_df), '\n', sep = '')
