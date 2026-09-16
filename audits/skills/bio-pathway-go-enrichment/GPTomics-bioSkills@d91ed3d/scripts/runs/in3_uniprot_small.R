# go-enrichment Input 3 (edge): proteomics IDs are UniProt accessions and the hit list is small (15 proteins).
# SKILL.md "Build the Foreground and Universe from DE Results" block (b02) is written for SYMBOL; here the agent must map
# UNIPROT -> ENTREZID with bitr. Data: SYNTHETIC hit assignment over REAL org.Hs.eg.db annotations.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({library(clusterProfiler); library(org.Hs.eg.db)})
GG <- 'F:/OpenScience/audits/bio-pathway-go-enrichment'
tab <- read.csv(file.path(GG, 'data', 'proteomics_da_table.csv'), colClasses = 'character')
tab <- tab[!is.na(tab$uniprot) & tab$uniprot != '', ]
set.seed(3)
sig_up <- head(tab$uniprot[tab$hit_signal == 'TRUE'], 15)      # a small hit list, as a 250 pg or targeted run gives
all_up <- tab$uniprot
cat('foreground accessions', length(sig_up), '| universe accessions', length(all_up), '\n')
fg <- tryCatch(bitr(sig_up, fromType = 'UNIPROT', toType = 'ENTREZID', OrgDb = org.Hs.eg.db), error = function(e) { cat('bitr ERROR:', conditionMessage(e), '\n'); NULL })
bg <- bitr(all_up, fromType = 'UNIPROT', toType = 'ENTREZID', OrgDb = org.Hs.eg.db)
cat('foreground mapped rows', nrow(fg), 'unique entrez', length(unique(fg$ENTREZID)),
    '| conversion loss:', round(100 * (1 - length(unique(fg$UNIPROT)) / length(sig_up)), 1), '%\n')
cat('universe mapped rows', nrow(bg), 'unique entrez', length(unique(bg$ENTREZID)),
    '| one-to-many inflation rows:', nrow(bg) - length(unique(bg$UNIPROT)), '\n')
gene_list <- unique(fg$ENTREZID); universe_ids <- unique(bg$ENTREZID)
blk <- list.files(file.path(GG, 'runs', 'blocks'), pattern = '^b01', full.names = TRUE)
res <- tryCatch({ sys.source(blk, envir = globalenv()); 'OK' }, error = function(e) paste('ERROR:', conditionMessage(e)))
cat('[enrichGO block verbatim, 15-protein list]', res, '\n')
d <- as.data.frame(ego); cat('terms at p.adjust<0.05:', nrow(d), '\n')
# the Skill says an empty table usually means the cutoff or the universe: inspect with cutoffs at 1
ego_all <- enrichGO(gene = gene_list, universe = universe_ids, OrgDb = org.Hs.eg.db, keyType = 'ENTREZID', ont = 'BP',
                    pAdjustMethod = 'BH', pvalueCutoff = 1, qvalueCutoff = 1, minGSSize = 10, maxGSSize = 500, readable = TRUE)
da <- as.data.frame(ego_all)
cat('terms with cutoffs at 1:', nrow(da), '| min raw p:', signif(min(da$pvalue), 3), '| min p.adjust:', signif(min(da$p.adjust), 3), '\n')
if (nrow(da)) print(head(da[order(da$pvalue), c('ID', 'Description', 'GeneRatio', 'BgRatio', 'pvalue', 'p.adjust')], 5))
