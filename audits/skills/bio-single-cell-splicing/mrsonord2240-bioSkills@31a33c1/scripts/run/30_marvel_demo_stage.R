# INPUT 4 (real data): stage the inputs SKILL.md block S04 expects, FROM THE REAL Smart-seq2 demo object shipped in the MARVEL package (iPSC vs endoderm, 30 cells).
# Cell types are renamed iPSC -> neuron, Endoderm -> glia so S04 can be run WITHOUT editing it. Per-cell STAR SJ.out.tab files are re-written from the package's junction matrix.
suppressMessages({library(MARVEL); library(data.table); library(Seurat)})
m <- readRDS(system.file('extdata/data/marvel.demo.rds', package='MARVEL'))
D <- 'F:/OpenScience/audits/bio-single-cell-splicing/run/out/in4_demo'; dir.create(file.path(D, 'star_pass2'), showWarnings=FALSE, recursive=TRUE)
sj <- m$SpliceJunction
for (cell in colnames(sj)[-1]) {
  v <- sj[[cell]]; ok <- !is.na(v) & v > 0
  p <- do.call(rbind, strsplit(sj$coord.intron[ok], ':'))
  d <- data.frame(chr=p[,1], start=p[,2], end=p[,3], strand=0, motif=1, annot=1, unique=v[ok], multi=0, overhang=30)
  write.table(d, file.path(D, 'star_pass2', paste0(cell, '_SJ.out.tab')), sep='\t', quote=FALSE, row.names=FALSE, col.names=FALSE)
}
for (ev in c('SE', 'MXE', 'RI', 'A5SS', 'A3SS')) write.table(m$SpliceFeature[[ev]], file.path(D, paste0('events_', ev, '.txt')), sep='\t', quote=FALSE, row.names=FALSE)
write.table(m$GeneFeature, file.path(D, 'gene_features.tsv'), sep='\t', quote=FALSE, row.names=FALSE)
write.table(m$Exp, file.path(D, 'tpm.tsv'), sep='\t', quote=FALSE, row.names=FALSE)
write.table(m$GTF, file.path(D, 'annotation.gtf'), sep='\t', quote=FALSE, row.names=FALSE, col.names=FALSE)
cnt <- as.matrix(m$Exp[, -1]); rownames(cnt) <- make.unique(as.character(m$Exp$gene_id)); cnt <- round(2^cnt)
ct <- ifelse(m$SplicePheno$cell.type == 'iPSC', 'neuron', 'glia')
so <- CreateSeuratObject(counts=cnt, meta.data=data.frame(cell.type=ct, row.names=m$SplicePheno$sample.id))
saveRDS(so, file.path(D, 'cells.rds'))
cat('staged', length(list.files(D, recursive=TRUE)), 'files; cell types:\n'); print(table(so@meta.data$cell.type))
cat('demo event-table sizes:', paste(names(m$SpliceFeature), sapply(m$SpliceFeature, function(x) if (is.null(x)) 0 else nrow(x)), collapse=' '), '\n')
