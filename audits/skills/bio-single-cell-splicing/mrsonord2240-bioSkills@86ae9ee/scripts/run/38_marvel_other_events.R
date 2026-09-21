# Unrun-by-fixer items: MARVEL ComputePSI for MXE / A5SS / A3SS / RI (RI needs IntronCounts) and CompareValues method='dts', on the REAL package demo (Smart-seq2, 30 cells).
suppressMessages({library(MARVEL)}); options(warn = 1)
m <- readRDS(system.file('extdata/data/marvel.demo.rds', package = 'MARVEL'))
cat('demo object slots:', paste(names(m), collapse = ','), '\n'); cat('demo PSI slot present:', !is.null(m$PSI), if (!is.null(m$PSI)) paste(names(m$PSI), collapse = ','), '\n')
build <- function(intron = TRUE) CreateMarvelObject(SpliceJunction = m$SpliceJunction, SplicePheno = m$SplicePheno, SpliceFeature = m$SpliceFeature, IntronCounts = if (intron) m$IntronCounts else NULL, GeneFeature = m$GeneFeature, Exp = m$Exp)
mm <- build(TRUE)
for (ev in c('SE', 'MXE', 'A5SS', 'A3SS', 'RI')) {
  r <- tryCatch({ x <- ComputePSI(mm, CoverageThreshold = 10, EventType = ev); p <- x$PSI[[ev]]
    cells <- setdiff(colnames(p), c('tran_id', 'gene_id', 'gene_short_name', 'gene_type', 'event_type')); v <- as.matrix(p[, cells])
    ref <- if (!is.null(m$PSI[[ev]])) { q <- m$PSI[[ev]]; q <- q[match(p$tran_id, q$tran_id), cells]; max(abs(as.matrix(q) - v), na.rm = TRUE) } else NA
    sprintf('ComputePSI %-4s OK: %d events x %d cells, non-NA fraction %.2f, range %.3f-%.3f; max|diff| vs package-shipped PSI %s', ev, nrow(p), length(cells), mean(!is.na(v)), min(v, na.rm = TRUE), max(v, na.rm = TRUE), format(ref)) },
    error = function(e) paste('ComputePSI', ev, 'ERROR:', conditionMessage(e)))
  cat(r, '\n')
}
mm2 <- build(FALSE); r <- tryCatch({ ComputePSI(mm2, CoverageThreshold = 10, EventType = 'RI'); 'RI without IntronCounts: NO ERROR' }, error = function(e) paste('RI without IntronCounts ERROR:', conditionMessage(e))); cat(r, '\n')
# CompareValues on A5SS with wilcox and dts
mm <- ComputePSI(mm, CoverageThreshold = 10, EventType = 'A5SS'); mm <- CheckAlignment(mm, level = 'SJ'); 
ph <- m$SplicePheno; g1 <- ph$sample.id[ph$cell.type == unique(ph$cell.type)[1]]; g2 <- ph$sample.id[ph$cell.type == unique(ph$cell.type)[2]]
for (meth in c('wilcox', 'dts')) { r <- tryCatch({ x <- CompareValues(mm, cell.group.g1 = g1, cell.group.g2 = g2, min.cells = 5, method = meth, level = 'splicing', event.type = 'A5SS', show.progress = FALSE); sprintf('CompareValues A5SS %s OK: %d rows', meth, nrow(x$DE$PSI$Table[[meth]])) }, error = function(e) paste('CompareValues A5SS', meth, 'ERROR:', conditionMessage(e))); cat(r, '\n') }
cat('twosamples installed:', requireNamespace('twosamples', quietly = TRUE), '\n')
