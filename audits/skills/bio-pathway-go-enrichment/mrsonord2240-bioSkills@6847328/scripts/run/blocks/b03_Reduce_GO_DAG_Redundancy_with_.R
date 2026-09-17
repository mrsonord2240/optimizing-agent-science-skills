ego_bp <- enrichGO(gene_list, universe = universe_ids, OrgDb = org.Hs.eg.db, keyType = 'ENTREZID', ont = 'BP', readable = TRUE)
ego_bp <- simplify(ego_bp, cutoff = 0.7, by = 'p.adjust', select_fun = min, measure = 'Wang')
