# go-enrichment Input 3 (Edge, regression of pre-fix Input 3): UniProt accessions,
# a 15-protein hit list. bitr UNIPROT->ENTREZID per SKILL.md's "Build the Foreground and
# Universe" pattern, then block b01 verbatim. Also checks the pvalueCutoff-filters-p.adjust
# claim by inspecting with cutoffs at 1.
suppressPackageStartupMessages({library(clusterProfiler); library(org.Hs.eg.db)})
GG <- 'F:/OpenScience/audits/bio-pathway-go-enrichment'
tab <- read.csv(file.path(GG, 'data', 'proteomics_da_table.csv'), colClasses = 'character')
tab$hit_signal <- tab$hit_signal == 'TRUE'

# Build the foreground so a 15-protein edge case still carries the planted GO:0002181
# (cytoplasmic translation) signal: prioritize hits that are translation-annotated,
# fill the rest randomly, exactly mirroring the "small but real signal" edge case the
# pre-fix audit used.
trans <- unique(AnnotationDbi::select(org.Hs.eg.db, keys = 'GO:0002181', keytype = 'GOALL', columns = 'ENTREZID')$ENTREZID)
tab$is_trans <- tab$entrez %in% trans
sig_trans_uniprot <- unique(na.omit(tab$uniprot[tab$hit_signal & tab$is_trans]))
sig_other_uniprot <- unique(na.omit(tab$uniprot[tab$hit_signal & !tab$is_trans]))
set.seed(3)
n_trans <- min(8, length(sig_trans_uniprot))
fg15 <- c(sample(sig_trans_uniprot, n_trans), sample(sig_other_uniprot, 15 - n_trans))
bg_uniprot <- unique(na.omit(tab$uniprot))

fg_map <- bitr(fg15, fromType = 'UNIPROT', toType = 'ENTREZID', OrgDb = org.Hs.eg.db)
bg_map <- bitr(bg_uniprot, fromType = 'UNIPROT', toType = 'ENTREZID', OrgDb = org.Hs.eg.db)
cat('foreground UniProt:', length(fg15), '-> mapped rows:', nrow(fg_map), '| conversion rate:', round(100*length(unique(fg_map$UNIPROT))/length(fg15),1), '%\n')
cat('universe UniProt:', length(bg_uniprot), '-> mapped rows (pre-dedup):', nrow(bg_map), '\n')

gene_list <- unique(fg_map$ENTREZID)
universe_ids <- unique(bg_map$ENTREZID)
cat('deduplicated: foreground', length(gene_list), '| universe', length(universe_ids), '(dropped', nrow(bg_map)-length(universe_ids), 'duplicate rows)\n')

blk <- list.files(file.path(GG, 'runs', 'blocks'), pattern = '^b01', full.names = TRUE)
sys.source(blk, envir = globalenv())
d <- as.data.frame(ego)
cat('terms at default cutoffs:', nrow(d), '\n')
if (nrow(d)) print(d[, c('ID','Description','GeneRatio','p.adjust')])
cat('planted term present:', 'GO:0002181' %in% d$ID, '\n')

ego_all <- enrichGO(gene = gene_list, universe = universe_ids, OrgDb = org.Hs.eg.db, keyType = 'ENTREZID',
                     ont = 'BP', pAdjustMethod = 'BH', pvalueCutoff = 1, qvalueCutoff = 1, readable = TRUE)
d_all <- as.data.frame(ego_all)
cat('terms with cutoffs at 1:', nrow(d_all), '\n')
cat('min raw p:', min(d_all$pvalue), '| min p.adjust:', min(d_all$p.adjust), '\n')
