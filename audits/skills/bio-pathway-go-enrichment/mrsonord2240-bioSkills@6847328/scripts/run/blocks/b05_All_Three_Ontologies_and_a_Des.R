ego_all <- enrichGO(gene_list, universe = universe_ids, OrgDb = org.Hs.eg.db, keyType = 'ENTREZID', ont = 'ALL', readable = TRUE)
ggo     <- groupGO(gene_list, OrgDb = org.Hs.eg.db, keyType = 'ENTREZID', ont = 'BP', level = 3, readable = TRUE)
