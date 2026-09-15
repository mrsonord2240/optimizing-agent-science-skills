.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({library(proDA); library(DEqMS)})
src <- deparse(proDA::test_diff); cat(grep('df', src, value = TRUE), sep = '\n')
cat('\n---- DEqMS::spectraCounteBayes ----\n'); print(DEqMS::spectraCounteBayes)
