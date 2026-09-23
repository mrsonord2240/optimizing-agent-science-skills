# Input 11: exercise current Stage 2 script twice on fixed synthetic data and compare output.
make_input <- function() {
  set.seed(20260923)
  n_features <- 80L
  sample_class <<- c(rep('QC', 6), rep(c('Control', 'Treatment'), each = 6))
  injection_order <<- seq_along(sample_class)
  batch_id <<- rep(1L, length(sample_class))
  feat <<- matrix(2^rnorm(n_features * length(sample_class), 14, 0.25), nrow = n_features)
  feat[1:8, sample_class == 'Treatment'] <<- feat[1:8, sample_class == 'Treatment'] * 2
  feat[cbind(rep(1:3, each = 2), c(8, 9, 10, 11, 12, 13))] <<- NA_real_
  rownames(feat) <<- paste0('FT', seq_len(n_features)); colnames(feat) <<- paste0('S', seq_along(sample_class))
  defs <<- data.frame(mzmed = seq_len(n_features), rtmed = seq_len(n_features), row.names = rownames(feat))
}
run_once <- function() {
  make_input()
  source('F:/OpenScience/wt/workflows-metabolomics-pipeline/workflows/metabolomics-pipeline/scripts/stage2_qc_impute.R')
  imputed
}
a <- run_once(); b <- run_once()
stopifnot(!anyNA(a), identical(a, b), min(a) >= 0)
cat('Stage 2 determinism PASS:', nrow(a), 'features x', ncol(a), 'samples; two seeded runs byte-identical.\n')
