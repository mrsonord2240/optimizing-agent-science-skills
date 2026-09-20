# Build the Skill's MARVEL inputs (STAR SJ.out.tab per cell, event tables, gene features, TPM, Seurat object) FROM THE PACKAGE'S OWN REAL DEMO (Smart-seq2 iPSC vs endoderm, 30 cells).
suppressMessages({library(MARVEL); library(data.table); library(Seurat)})
m <- readRDS(system.file('extdata/data/marvel.demo.rds', package='MARVEL'))
D <- 'F:/OpenScience/audits/bio-single-cell-splicing/run/data/marvel_star'; dir.create(D, showWarnings=FALSE, recursive=TRUE)
dir.create(file.path(D,'star_pass2'), showWarnings=FALSE)
sj <- m$SpliceJunction
cat('demo SJ NA fraction:', mean(is.na(sj[,-1])), ' zero fraction:', mean(sj[,-1]==0, na.rm=TRUE), '\n')
for (cell in colnames(sj)[-1]) {
  v <- sj[[cell]]; ok <- !is.na(v) & v > 0
  p <- do.call(rbind, strsplit(sj$coord.intron[ok], ':'))
  d <- data.frame(chr=p[,1], start=p[,2], end=p[,3], strand=0, motif=1, annot=1, unique=v[ok], multi=0, overhang=30)
  write.table(d, file.path(D,'star_pass2', paste0(cell, '_SJ.out.tab')), sep='\t', quote=FALSE, row.names=FALSE, col.names=FALSE)
}
for (ev in names(m$SpliceFeature)) if (!is.null(m$SpliceFeature[[ev]])) write.table(m$SpliceFeature[[ev]], file.path(D, paste0('events_', ev, '.txt')), sep='\t', quote=FALSE, row.names=FALSE)
write.table(m$GeneFeature, file.path(D,'gene_features.tsv'), sep='\t', quote=FALSE, row.names=FALSE)
write.table(m$Exp, file.path(D,'tpm.tsv'), sep='\t', quote=FALSE, row.names=FALSE)   # demo Exp has gene_id as first column
saveRDS(m$GTF, file.path(D,'gtf_df.rds'))
# Seurat object with cell types in meta.data (the Skill reads 'cells.rds')
cnt <- as.matrix(m$Exp[,-1]); rownames(cnt) <- make.unique(as.character(m$Exp$gene_id)); cnt <- round(2^cnt)
so <- CreateSeuratObject(counts=cnt, meta.data=data.frame(cell.type=m$SplicePheno$cell.type, row.names=m$SplicePheno$sample.id))
saveRDS(so, file.path(D,'cells.rds'))
cat('files:', length(list.files(D, recursive=TRUE)), '\n'); print(table(so@meta.data$cell.type))
print(head(m$SpliceFeature$SE$tran_id,2)); print(sapply(m$SpliceFeature, function(x) if(is.null(x)) 0 else nrow(x)))
print(head(m$IntronCounts[,1:3],2))
