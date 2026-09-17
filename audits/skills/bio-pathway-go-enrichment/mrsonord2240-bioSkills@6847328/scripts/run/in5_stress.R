# go-enrichment Input 5 (Stress, regression of pre-fix Input 5): direction-split ORA,
# fold enrichment, redundancy collapse, and a custom gene set via enricher(). Blocks b01,
# b03 and b06 verbatim in spirit.
suppressPackageStartupMessages({library(clusterProfiler); library(org.Hs.eg.db)})
GG <- 'F:/OpenScience/audits/bio-pathway-go-enrichment'
tab <- read.csv(file.path(GG, 'data', 'proteomics_da_table.csv'), colClasses = 'character')
tab$hit_signal <- tab$hit_signal == 'TRUE'
tab$log2FC <- as.numeric(tab$log2FC)
universe_ids <- unique(tab$entrez)
up_genes   <- unique(tab$entrez[tab$hit_signal & tab$log2FC > 0])
down_genes <- unique(tab$entrez[tab$hit_signal & tab$log2FC < 0])
mixed_genes <- unique(tab$entrez[tab$hit_signal])
cat('up:', length(up_genes), '| down:', length(down_genes), '| mixed:', length(mixed_genes), '\n')

run <- function(g) enrichGO(gene = g, universe = universe_ids, OrgDb = org.Hs.eg.db, keyType = 'ENTREZID',
                             ont = 'BP', pAdjustMethod = 'BH', pvalueCutoff = 0.05, qvalueCutoff = 0.2, readable = TRUE)
ego_up <- run(up_genes); ego_down <- run(down_genes); ego_mixed <- run(mixed_genes)
d_up <- as.data.frame(ego_up); d_down <- as.data.frame(ego_down); d_mixed <- as.data.frame(ego_mixed)
cat('up terms:', nrow(d_up), '| down terms:', nrow(d_down), '| mixed terms:', nrow(d_mixed), '\n')
cat('planted term FoldEnrichment  up:', d_up$FoldEnrichment[d_up$ID=='GO:0002181'],
    '  down:', if('GO:0002181' %in% d_down$ID) d_down$FoldEnrichment[d_down$ID=='GO:0002181'] else NA, '\n')

simp_up <- simplify(ego_up, cutoff = 0.7, by = 'p.adjust', select_fun = min, measure = 'Wang')
simp_down_n <- if (nrow(d_down) > 0) nrow(as.data.frame(simplify(ego_down, cutoff = 0.7, by = 'p.adjust', select_fun = min, measure = 'Wang'))) else 0
cat('simplify: up', nrow(d_up), '->', nrow(as.data.frame(simp_up)), '| down', nrow(d_down), '->', simp_down_n, '\n')

# custom TERM2GENE (120-row) built from a real GO term the enricher() route can score independently
t2g <- data.frame(term = 'CUSTOM_TRANSLATION_SET', gene = sample(universe_ids, 120))
t2g$gene[1:30] <- sample(mixed_genes, min(30, length(mixed_genes)))  # plant overlap with the hit list
ec <- enricher(mixed_genes, TERM2GENE = t2g, universe = universe_ids, pvalueCutoff = 0.05, pAdjustMethod = 'BH', minGSSize = 1, maxGSSize = 500, qvalueCutoff = 0.2)
d_ec <- as.data.frame(ec)
cat('enricher() custom set: terms =', nrow(d_ec), '\n')
if (nrow(d_ec)) print(d_ec[, c('ID','GeneRatio','BgRatio','RichFactor','FoldEnrichment','zScore','p.adjust','Count')])
cat('enricher() output has the same RichFactor/FoldEnrichment/zScore columns as enrichGO:',
    all(c('RichFactor','FoldEnrichment','zScore') %in% colnames(d_ec)), '\n')
