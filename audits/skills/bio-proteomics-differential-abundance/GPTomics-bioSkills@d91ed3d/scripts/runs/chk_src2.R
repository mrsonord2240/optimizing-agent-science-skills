.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({library(proDA); library(DEqMS)})
ns <- asNamespace('proDA'); fns <- ls(ns)
for (f in fns) { s <- deparse(get(f, ns)); if (any(grepl('n_approx', s)) && any(grepl('df', s))) { cat('==', f, '\n'); cat(grep('df|n_approx', s, value = TRUE), sep = '\n') } }
cat('\n---- DEqMS::outputResult ----\n'); print(DEqMS::outputResult)
