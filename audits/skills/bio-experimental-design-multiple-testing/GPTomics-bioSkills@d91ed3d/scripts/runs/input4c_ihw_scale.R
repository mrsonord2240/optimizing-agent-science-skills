.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressMessages(library(IHW))
d <- read.csv('F:/OpenScience/audits/bio-experimental-design-multiple-testing/data/synthetic_de_pvalues.csv')
for (m in c(5000, 8000, 12000, 18000)) {
  cat('m =', m, ' positional ihw() ... '); flush.console()
  r <- ihw(d$pvalue[1:m], d$mean_expression[1:m], alpha = 0.05)
  cat('OK rejections =', rejections(r), ' nbins =', nbins(r), '\n'); flush.console()
}
