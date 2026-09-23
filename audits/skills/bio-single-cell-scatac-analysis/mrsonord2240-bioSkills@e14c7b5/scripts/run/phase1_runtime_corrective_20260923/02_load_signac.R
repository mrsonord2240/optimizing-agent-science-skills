# Windows R runtime exit probe: exact private library plus minimal Signac load.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages(library(Signac))
cat('PROBE_LOAD_SIGNAC_OK ', as.character(packageVersion('Signac')), '\n', sep = '')
quit(save = 'no', status = 0, runLast = FALSE)
