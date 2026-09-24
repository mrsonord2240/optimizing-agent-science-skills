# Why does ComputePSI(EventType='RI') fail with 'argument is of length zero'? Print the RI-related formals, then retry with the extra arguments (thread, read.length).
suppressMessages(library(MARVEL)); print(formals(MARVEL::ComputePSI))
m <- readRDS(system.file('extdata/data/marvel.demo.rds', package = 'MARVEL'))
mm <- CreateMarvelObject(SpliceJunction = m$SpliceJunction, SplicePheno = m$SplicePheno, SpliceFeature = m$SpliceFeature, IntronCounts = m$IntronCounts, GeneFeature = m$GeneFeature, Exp = m$Exp)
for (th in c(1, 2)) for (rl in c(50, 100)) { r <- tryCatch({x <- ComputePSI(mm, CoverageThreshold = 10, EventType = 'RI', thread = th, read.length = rl); v <- x$PSI$RI; paste('OK', nrow(v), 'events; non-NA', round(mean(!is.na(as.matrix(v[, -(1:4)]))), 2))}, error=function(e) conditionMessage(e)); cat('thread', th, 'read.length', rl, ':', r, '\n') }
x <- ComputePSI(mm, CoverageThreshold = 10, EventType = 'RI', thread = 2, read.length = 100); p <- x$PSI$RI; cells <- setdiff(colnames(p), c('tran_id','gene_id','gene_short_name','gene_type','event_type'))
cat('vs package-shipped PSI RI, max|diff|:', max(abs(as.matrix(p[, cells]) - as.matrix(m$PSI$RI[match(p$tran_id, m$PSI$RI$tran_id), cells])), na.rm = TRUE), '\n')
