.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
d <- readRDS('F:/OpenScience/audits/_pre-fix-20260923/bio-single-cell-multimodal-integration/data/synthetic_multiome.rds')
str(d, max.level = 1)
for (n in names(d)) { cat(n, ':', paste(dim(d[[n]]), collapse='x'), '\n') }
