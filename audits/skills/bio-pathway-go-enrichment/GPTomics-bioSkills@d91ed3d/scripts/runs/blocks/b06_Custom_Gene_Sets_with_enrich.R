ego_custom <- enricher(gene_list, TERM2GENE = t2g, universe = universe_ids,
                       pvalueCutoff = 0.05, pAdjustMethod = 'BH', minGSSize = 10, maxGSSize = 500, qvalueCutoff = 0.2)
