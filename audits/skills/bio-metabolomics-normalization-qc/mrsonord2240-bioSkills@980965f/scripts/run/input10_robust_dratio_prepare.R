# Phase 2 Input 10 (new): verify the newly shipped robust D-ratio filter both as a sourced
# function and as a CLI on planted clean/noisy features. Generates a small non-sensitive CSV
# consumed by input10_robust_dratio_cli.sh.
set.seed(20260923)
source('F:/OpenScience/wt/metabolomics-normalization-qc/metabolomics/normalization-qc/scripts/robust_dratio_filter.R')

n_qc <- 12
n_bio <- 24
n_clean <- 30
n_noisy <- 30
base_clean <- seq(100, 130, length.out = n_clean)
base_noisy <- seq(140, 170, length.out = n_noisy)
# Planted clean features: stable QCs but broad biological spread -> low technical/biological D-ratio.
clean <- rbind(
  matrix(rep(base_clean, each = n_qc), nrow = n_qc) + matrix(rnorm(n_qc * n_clean, sd = 0.10), nrow = n_qc),
  matrix(rep(base_clean, each = n_bio), nrow = n_bio) + matrix(rnorm(n_bio * n_clean, sd = 20), nrow = n_bio)
)
# Planted noisy features: large QC variation but tight biological spread -> high D-ratio.
noisy <- rbind(
  matrix(rep(base_noisy, each = n_qc), nrow = n_qc) + matrix(rnorm(n_qc * n_noisy, sd = 35), nrow = n_qc),
  matrix(rep(base_noisy, each = n_bio), nrow = n_bio) + matrix(rnorm(n_bio * n_noisy, sd = 5), nrow = n_bio)
)
data <- cbind(clean, noisy)
colnames(data) <- c(paste0('clean_', seq_len(n_clean)), paste0('noisy_', seq_len(n_noisy)))
is_qc <- c(rep(TRUE, n_qc), rep(FALSE, n_bio))

kept <- robust_dratio_filter(data, is_qc, dratio_max = 0.5, rsd_max = 0.3)
stopifnot(identical(colnames(kept), paste0('clean_', seq_len(n_clean))))
cat(sprintf('Sourced function: kept %d/%d features; clean=%d noisy=%d\n', ncol(kept), ncol(data), sum(grepl('^clean_', colnames(kept))), sum(grepl('^noisy_', colnames(kept)))))

tbl <- data.frame(sample_type = ifelse(is_qc, 'QC', 'Sample'), data, check.names = FALSE)
write.csv(tbl, 'F:/OpenScience/audits/bio-metabolomics-normalization-qc/run/input10_peaks.csv', row.names = FALSE)
