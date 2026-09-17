library(clusterProfiler)
library(org.Hs.eg.db)

ego <- enrichGO(gene          = gene_list,        # foreground ENTREZ IDs
                universe      = universe_ids,     # tested-gene set, mapped identically -- NOT the genome
                OrgDb         = org.Hs.eg.db,
                keyType       = 'ENTREZID',
                ont           = 'BP',             # SET explicitly: source default is 'MF', not 'BP'
                pAdjustMethod = 'BH',
                pvalueCutoff  = 0.05,             # filters p.adjust (despite the name), not raw pvalue
                qvalueCutoff  = 0.2,
                minGSSize     = 10,
                maxGSSize     = 500,
                readable      = TRUE)             # map ENTREZ -> SYMBOL in the output
