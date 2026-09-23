# Phase 2 Input 12 (new edge): test the shipped QCRSC all-NA guard on a mixed-QC multi-batch run.
# Batch 1 is valid (8 QCs); batch 2 is below minQC (3 QCs). The Skill says to check per batch,
# but its copy-paste guard aggregates across the whole output.
library(pmp)
set.seed(20260923)
n_features <- 60
n1 <- 30; n2 <- 30
q1 <- 8; q2 <- 3
batch <- c(rep('B1', n1), rep('B2', n2))
classes <- c(rep('QC', q1), rep('Sample', n1 - q1), rep('QC', q2), rep('Sample', n2 - q2))
inj_order <- seq_len(n1 + n2)
mat <- matrix(exp(rnorm(n_features * (n1 + n2), mean = 5, sd = 0.2)), nrow = n_features)
colnames(mat) <- paste0('S', seq_len(ncol(mat)))

corrected <- QCRSC(df = mat, order = inj_order, batch = batch, classes = classes,
                   spar = 0, log = TRUE, minQC = 5, qc_label = 'QC')
out_mat <- if (methods::is(corrected, 'SummarizedExperiment')) SummarizedExperiment::assay(corrected) else corrected
global_guard <- any(rowSums(!is.na(out_mat)) > 0)
all_na_by_batch <- vapply(unique(batch), function(b) all(is.na(out_mat[, batch == b, drop = FALSE])), logical(1))
cat(sprintf('Global documented guard result: %s\n', global_guard))
cat(sprintf('All-NA by batch: %s\n', paste(sprintf('%s=%s', names(all_na_by_batch), all_na_by_batch), collapse = ', ')))
stopifnot(global_guard, isFALSE(all_na_by_batch[['B1']]), isTRUE(all_na_by_batch[['B2']]))
cat('PROVED: the global guard passes although the sparse-QC batch is entirely NA; a per-batch guard is required.\n')
