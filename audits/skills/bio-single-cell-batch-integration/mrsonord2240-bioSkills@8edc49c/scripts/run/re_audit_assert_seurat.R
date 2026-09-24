# Assert the source Seurat script emitted its intended integrated reduction.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages(library(Seurat))
obj <- readRDS('F:/OpenScience/audits/bio-single-cell-batch-integration/run/re_audit_seurat.rds')
stopifnot('integrated.rpca' %in% Reductions(obj), ncol(obj) == 400L, nlevels(Idents(obj)) > 1L)
cat(sprintf('PASS Seurat: %d cells, %d clusters, reductions=%s\n', ncol(obj), nlevels(Idents(obj)), paste(Reductions(obj), collapse=', ')))
