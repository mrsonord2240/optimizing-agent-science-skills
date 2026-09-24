library(MARVEL); library(data.table)

gtf <- fread('annotation.gtf', header=FALSE, sep='\t', quote='', data.table=FALSE)   # same GTF as the rMATS run
for (ev in c('SE', 'MXE', 'RI', 'A5SS', 'A3SS')) {
    tab <- Preprocess_rMATS(read.table(sprintf('rmats_out/fromGTF.%s.txt', ev), header=TRUE, sep='\t'),
                            GTF=gtf, EventType=ev)
    write.table(tab, sprintf('events_%s.txt', ev), sep='\t', quote=FALSE, row.names=FALSE)
}
