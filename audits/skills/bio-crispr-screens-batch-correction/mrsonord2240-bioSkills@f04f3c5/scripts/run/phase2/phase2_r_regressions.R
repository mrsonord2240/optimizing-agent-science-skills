# Phase-2 independent regression runs for Input 2 (RUV) and Input 9 (SVA + NTC normalization).
suppressMessages(library(RUVSeq))
suppressMessages(library(sva))
set.seed(20260922)
script_arg <- commandArgs(trailingOnly = FALSE)[grep('^--file=', commandArgs(trailingOnly = FALSE))]
run_dir <- dirname(normalizePath(sub('^--file=', '', script_arg)))

samples <- paste0('S', 1:8)
batches <- rep(c('b1', 'b2'), each = 4)
condition <- rep(c('ctrl', 'ctrl', 'treat', 'treat'), 2)
n <- 1000
ntc <- 1:300
mu <- matrix(700, nrow = n, ncol = 8)
mu[, batches == 'b2'] <- 450
mu[301:360, condition == 'treat'] <- 120
counts_df <- matrix(rpois(n * 8, lambda = pmax(mu, 1)), nrow = n, dimnames = list(c(paste0('NT_', seq_len(300)), paste0('G_', seq_len(700))), samples))
ntc_sgrna_names <- rownames(counts_df)[ntc]

cat('INPUT 2 Variant A: RUVg character control-rowname dispatch\n')
ntc_rownames <- rownames(counts_df)[rownames(counts_df) %in% ntc_sgrna_names]
stopifnot(length(ntc_rownames) == 300)
seqset <- newSeqExpressionSet(counts = counts_df)
ruv_corrected <- RUVg(seqset, cIdx = ntc_rownames, k = 2)
W <- pData(ruv_corrected)
corrected_counts <- normCounts(ruv_corrected)
stopifnot(all(c('W_1', 'W_2') %in% colnames(W)), identical(dim(corrected_counts), dim(counts_df)), !anyNA(corrected_counts))
old <- try(RUVg(seqset, cIdx = which(rownames(counts_df) %in% ntc_sgrna_names), k = 2), silent = TRUE)
stopifnot(inherits(old, 'try-error'))
cat(sprintf('ASSERT input2: W=%dx%d, corrected=%dx%d, old integer cIdx rejected\n', nrow(W), ncol(W), nrow(corrected_counts), ncol(corrected_counts)))

cat('INPUT 9 Fresh: SVA factors and NTC-anchored normalization\n')
metadata <- data.frame(condition = factor(condition), row.names = samples)
mod <- model.matrix(~ condition, data = metadata)
mod0 <- model.matrix(~ 1, data = metadata)
sv_obj <- sva(counts_df, mod, mod0)
design_matrix <- cbind(mod, sv_obj$sv)
stopifnot(nrow(design_matrix) == 8, !anyNA(design_matrix))
ntc_anchored_normalize <- function(counts_df, ntc_sgrna_names, target_median = 1000) {
  ntc_counts <- counts_df[rownames(counts_df) %in% ntc_sgrna_names, , drop = FALSE]
  stopifnot(nrow(ntc_counts) >= 1)
  scale_factors <- target_median / apply(ntc_counts, 2, median)
  sweep(counts_df, 2, scale_factors, '*')
}
anchored <- ntc_anchored_normalize(counts_df, ntc_sgrna_names, target_median = 1000)
stopifnot(all(abs(apply(anchored[ntc_sgrna_names, , drop = FALSE], 2, median) - 1000) < 1e-9))
write.csv(corrected_counts, file.path(run_dir, 'input2_ruv_corrected.csv'))
write.csv(anchored, file.path(run_dir, 'input9_ntc_anchored.csv'))
cat(sprintf('ASSERT input9: n_sv=%d; design=%dx%d; all NTC medians exactly 1000\n', sv_obj$n.sv, nrow(design_matrix), ncol(design_matrix)))
cat('PHASE2_R_REGRESSIONS_PASS\n')
