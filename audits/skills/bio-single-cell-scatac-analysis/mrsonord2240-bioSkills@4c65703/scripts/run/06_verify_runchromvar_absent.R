.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({
  library(Signac)
})
cat('Signac version:', as.character(packageVersion('Signac')), '\n')
cat('RunChromVAR exists as exported function?', exists('RunChromVAR', where = asNamespace('Signac'), inherits = FALSE), '\n')
cat('RunChromVAR in search path after library(Signac)?', exists('RunChromVAR'), '\n')
ns_exports <- getNamespaceExports('Signac')
cat('Any exported name matching ChromVAR (case-insensitive)?\n')
print(ns_exports[grepl('chromvar', ns_exports, ignore.case = TRUE)])
res <- tryCatch({
  RunChromVAR
  'FOUND'
}, error = function(e) paste('ERROR:', conditionMessage(e)))
cat('Direct call attempt result:', res, '\n')
cat('DONE\n')
