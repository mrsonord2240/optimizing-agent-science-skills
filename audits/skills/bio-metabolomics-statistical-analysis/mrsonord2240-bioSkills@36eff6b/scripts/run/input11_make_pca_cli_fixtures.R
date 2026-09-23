# Fresh Phase 2 fixture generator for the documented pca_hotelling.R CLI.
# It writes features x samples CSVs: one valid matrix with two planted outliers,
# and one NA-containing matrix for the explicit upstream-imputation stop path.
set.seed(20260923)
out_dir <- 'F:/OpenScience/audits/bio-metabolomics-statistical-analysis/data'
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
n <- 48; p <- 120
x <- matrix(rnorm(n * p, mean = 10, sd = 1), nrow = n, ncol = p,
            dimnames = list(paste0('S', seq_len(n)), paste0('M', seq_len(p))))
x['S1', ] <- x['S1', ] + 18
x['S2', seq_len(40)] <- x['S2', seq_len(40)] - 22
write.csv(t(x), file.path(out_dir, 'input11_pca_valid.csv'), quote = FALSE)
x_na <- x
x_na['S3', 'M1'] <- NA_real_
write.csv(t(x_na), file.path(out_dir, 'input11_pca_has_na.csv'), quote = FALSE)
cat('Wrote valid and NA fixtures:', nrow(t(x)), 'features x', ncol(t(x)), 'samples\n')
