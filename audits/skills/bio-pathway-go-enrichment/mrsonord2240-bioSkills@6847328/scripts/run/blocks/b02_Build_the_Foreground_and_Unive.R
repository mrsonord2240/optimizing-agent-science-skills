de <- read.csv('de_results.csv')

sig_genes  <- de$gene_id[de$padj < 0.05 & abs(de$log2FoldChange) > 1]   # foreground = hits
all_tested <- de$gene_id[!is.na(de$pvalue)]                            # universe = tested genes, NOT all rows, NOT the genome

fg_map <- bitr(sig_genes,  fromType = 'SYMBOL', toType = 'ENTREZID', OrgDb = org.Hs.eg.db)
bg_map <- bitr(all_tested, fromType = 'SYMBOL', toType = 'ENTREZID', OrgDb = org.Hs.eg.db)

gene_list    <- unique(fg_map$ENTREZID)   # deduplicate one-to-many maps before counting
universe_ids <- unique(bg_map$ENTREZID)
