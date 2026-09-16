.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressMessages(library(qvalue))
set.seed(3)
n <- 0
for (r in 1:200) {
  pv <- runif(20)
  o <- try(qvalue(pv), silent = TRUE)
  if (inherits(o, 'try-error')) { n <- n + 1; if (n == 1) { cat('First failure, m=20. Verbatim error:\n'); cat(as.character(o)) } }
}
cat(sprintf('\nFailures: %d / 200 at m=20\n', n))
