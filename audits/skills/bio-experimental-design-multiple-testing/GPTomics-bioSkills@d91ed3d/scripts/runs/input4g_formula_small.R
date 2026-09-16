.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressMessages(library(IHW))
d <- read.csv('F:/OpenScience/audits/bio-experimental-design-multiple-testing/data/synthetic_de_pvalues.csv')
m <- as.integer(commandArgs(TRUE)[1]); dd <- d[1:m, ]
cat('formula interface, m =', m, '... '); flush.console()
r <- ihw(pvalue ~ mean_expression, data = dd, alpha = 0.05)
cat('OK rejections =', rejections(r), 'nbins =', nbins(r), '\n')
