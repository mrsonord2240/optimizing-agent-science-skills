g <- readRDS('F:/OpenScience/audits/bio-single-cell-splicing/run/data/marvel_star/gtf_df.rds')
print(head(g,2)); print(sapply(g, class))
write.table(g, 'F:/OpenScience/audits/bio-single-cell-splicing/run/data/marvel_star/annotation.gtf', sep='\t', quote=FALSE, row.names=FALSE, col.names=FALSE)
