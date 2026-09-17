# go-enrichment Input 2 (Variant A, regression of pre-fix Input 2): effect of omitting
# universe= on a null (no-biology) hit list, and on the signal list. Block b01 verbatim,
# then the same call with the universe line removed.
suppressPackageStartupMessages({library(clusterProfiler); library(org.Hs.eg.db)})
GG <- 'F:/OpenScience/audits/bio-pathway-go-enrichment'
tab <- read.csv(file.path(GG, 'data', 'proteomics_da_table.csv'), colClasses = 'character')
tab$hit_null <- tab$hit_null == 'TRUE'
tab$hit_signal <- tab$hit_signal == 'TRUE'
universe_ids <- unique(tab$entrez)

null_genes <- unique(tab$entrez[tab$hit_null])
sig_genes  <- unique(tab$entrez[tab$hit_signal])

run <- function(genes, universe) {
  enrichGO(gene = genes, universe = universe, OrgDb = org.Hs.eg.db, keyType = 'ENTREZID',
           ont = 'BP', pAdjustMethod = 'BH', pvalueCutoff = 0.05, qvalueCutoff = 0.2,
           minGSSize = 10, maxGSSize = 500, readable = TRUE)
}

null_matched <- as.data.frame(run(null_genes, universe_ids))
null_omitted <- as.data.frame(run(null_genes, NULL))
sig_matched  <- as.data.frame(run(sig_genes, universe_ids))
sig_omitted  <- as.data.frame(run(sig_genes, NULL))

cat('--- null hit list (no planted biology), 150 genes ---\n')
cat('matched universe: terms =', nrow(null_matched), '\n')
cat('universe omitted: terms =', nrow(null_omitted), '\n')
if (nrow(null_omitted)) print(null_omitted[, c('ID','Description','BgRatio','p.adjust')])
if (nrow(null_matched)) cat('N with matched universe (from BgRatio):', unique(sapply(strsplit(null_matched$BgRatio,'/'),`[`,2)), '\n')
if (nrow(null_omitted)) cat('N with universe omitted (from BgRatio):', unique(sapply(strsplit(null_omitted$BgRatio,'/'),`[`,2)), '\n')

cat('\n--- signal hit list (planted GO:0002181), 150 genes ---\n')
cat('matched universe: terms =', nrow(sig_matched), '\n')
cat('universe omitted: terms =', nrow(sig_omitted), '\n')
cat('shared term IDs:', length(intersect(sig_matched$ID, sig_omitted$ID)), '\n')
pm <- sig_matched$p.adjust[sig_matched$ID == 'GO:0002181']
po <- sig_omitted$p.adjust[sig_omitted$ID == 'GO:0002181']
cat('planted term p.adjust matched vs omitted universe:', pm, 'vs', po, '\n')
