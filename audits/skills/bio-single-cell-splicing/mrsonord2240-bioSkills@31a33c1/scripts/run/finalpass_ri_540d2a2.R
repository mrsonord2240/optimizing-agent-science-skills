suppressMessages(library(MARVEL))
m <- readRDS(system.file('extdata/data/marvel.demo.rds', package='MARVEL'))
x <- CreateMarvelObject(SpliceJunction=m$SpliceJunction, SplicePheno=m$SplicePheno,
  SpliceFeature=m$SpliceFeature, IntronCounts=m$IntronCounts,
  GeneFeature=m$GeneFeature, Exp=m$Exp)
x <- ComputePSI(x, CoverageThreshold=10, EventType='RI', thread=2, read.length=100)
stopifnot(!is.null(x$PSI$RI), nrow(x$PSI$RI) > 0)
cat('PASS RI rows=', nrow(x$PSI$RI), ' cells=', ncol(x$PSI$RI)-5, '\n', sep='')
