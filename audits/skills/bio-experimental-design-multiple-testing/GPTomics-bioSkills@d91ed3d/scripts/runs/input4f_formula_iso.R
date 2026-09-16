.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressMessages(library(IHW))
d <- read.csv('F:/OpenScience/audits/bio-experimental-design-multiple-testing/data/synthetic_de_pvalues.csv')
arg <- commandArgs(TRUE)[1]
cat('variant:', arg, '\n'); flush.console()
r <- switch(arg,
  "formula_nbins4" = ihw(pvalue ~ mean_expression, data = d, alpha = 0.05, nbins = 4),
  "formula_default"= ihw(pvalue ~ mean_expression, data = d, alpha = 0.05),
  "positional_4"   = ihw(d$pvalue, d$mean_expression, alpha = 0.05, nbins = 4),
  "positional_grp" = ihw(d$pvalue, groups_by_filter(d$mean_expression, 4), alpha = 0.05))
cat('OK rejections =', rejections(r), ' nbins =', nbins(r), '\n')
