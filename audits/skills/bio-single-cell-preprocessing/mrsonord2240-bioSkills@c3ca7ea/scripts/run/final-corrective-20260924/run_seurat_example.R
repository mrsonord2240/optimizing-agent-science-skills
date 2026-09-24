.libPaths(c(
  'F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib',
  .libPaths()
))

setwd('F:/OpenScience/audits/bio-single-cell-preprocessing/run/final-corrective-20260924/seurat-example')
source(
  'F:/OpenScience/worktrees/bio-single-cell-preprocessing-fixpass/single-cell/preprocessing/examples/preprocess_seurat.R',
  echo = FALSE
)

stopifnot(file.exists('preprocessed.rds'))
obj <- readRDS('preprocessed.rds')
stopifnot(ncol(obj) == 658, length(VariableFeatures(obj)) == 3000)
cat('PASS: packaged Seurat example produced 658 cells and 3000 variable features\n')
