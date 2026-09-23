# Phase 2 input 5: UniProt ID conversion and local custom TERM2GENE enrichment.
suppressPackageStartupMessages({
  library(clusterProfiler)
  library(org.Hs.eg.db)
})
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
