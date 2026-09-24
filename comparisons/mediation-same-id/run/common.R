D <- 'F:/OpenScience/comparisons/mediation-same-id/data'
O <- 'F:/OpenScience/comparisons/mediation-same-id/out'
truth <- readRDS(file.path(D, 'truth.rds'))
try_run <- function(label, expr) {
  t0 <- Sys.time()
  r <- tryCatch(withCallingHandlers(expr, warning = function(w) { cat('  [warning]', label, ':', conditionMessage(w), '\n'); invokeRestart('muffleWarning') }),
                error = function(e) { cat('  [ERROR]', label, ':', conditionMessage(e), '\n'); NULL })
  cat(sprintf('  (%s: %.1fs)\n', label, as.numeric(difftime(Sys.time(), t0, units = 'secs'))))
  r
}
