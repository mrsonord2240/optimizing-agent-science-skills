# Does the RI PSI depend on read.length, and which value reproduces the package-shipped RI PSI?
suppressMessages(library(MARVEL)); m <- readRDS(system.file('extdata/data/marvel.demo.rds', package = 'MARVEL'))
mm <- CreateMarvelObject(SpliceJunction = m$SpliceJunction, SplicePheno = m$SplicePheno, SpliceFeature = m$SpliceFeature, IntronCounts = m$IntronCounts, GeneFeature = m$GeneFeature, Exp = m$Exp)
for (rl in c(1, 25, 50, 75, 100, 125, 150)) { invisible(capture.output(x <- ComputePSI(mm, CoverageThreshold = 10, EventType = 'RI', thread = 2, read.length = rl))); p <- x$PSI$RI
  cells <- setdiff(colnames(p), c('tran_id','gene_id','gene_short_name','gene_type','event_type')); ref <- m$PSI$RI[match(p$tran_id, m$PSI$RI$tran_id), cells]
  cat('read.length', rl, ' max|diff| vs shipped', round(max(abs(as.matrix(p[, cells]) - as.matrix(ref)), na.rm = TRUE), 4), ' mean|diff|', round(mean(abs(as.matrix(p[, cells]) - as.matrix(ref)), na.rm = TRUE), 4), '\n') }
