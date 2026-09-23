# Synthetic hg38 Ensembl DE table for literal execution of the SKILL.md GOseq block.
suppressPackageStartupMessages(library(org.Hs.eg.db))
id_map <- AnnotationDbi::select(
  org.Hs.eg.db,
  keys = AnnotationDbi::keys(org.Hs.eg.db, keytype = 'ENSEMBL'),
  keytype = 'ENSEMBL',
  columns = 'ENTREZID'
)
id_map <- id_map[!is.na(id_map$ENSEMBL) & !is.na(id_map$ENTREZID) &
                 !duplicated(id_map$ENSEMBL) & !duplicated(id_map$ENTREZID), ]
id_map <- id_map[seq_len(300L), ]
de <- data.frame(
  gene_id = id_map$ENSEMBL,
  pvalue = rep(0.1, nrow(id_map)),
  padj = c(rep(0.01, 50L), rep(0.5, nrow(id_map) - 50L)),
  log2FoldChange = c(rep(2, 50L), rep(0.1, nrow(id_map) - 50L))
)
