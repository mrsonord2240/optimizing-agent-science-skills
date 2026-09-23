# Phase 2 environment isolation: determine whether R crashes after a successful minimal DESeq2 session.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
library(DESeq2)
cat('minimal DESeq2 load: PASS\n')
