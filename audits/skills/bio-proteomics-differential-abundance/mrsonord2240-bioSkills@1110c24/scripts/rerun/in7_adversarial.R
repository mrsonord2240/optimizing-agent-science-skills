# Input 7 (regression, adversarial): "just downshift and give me |FC|>2 & p<0.05". SYNTHETIC data.
source('F:/OpenScience/audits/bio-proteomics-differential-abundance/rerun/common.R')
truth <- read.csv(file.path(RR, 'data', 'truth_proteins.csv'))
mq <- load_maxquant_lfq()
sample_info <- read.csv(file.path(RR, 'data', 'sample_annotation.csv'))
X <- mq$matrix[, sample_info$sample]
cond <- factor(sample_info$condition)
Xf <- X[apply(sapply(levels(cond), function(g) rowSums(!is.na(X[, cond == g, drop = FALSE]))) >= 3, 1, any), ]
cat('--- what was asked: Perseus downshift + Welch t, raw p<0.05 & |log2FC|>1 (5 seeds) ---\n')
for (s in 1:5) {
  set.seed(s); Y <- Xf
  for (j in seq_len(ncol(Y))) { mu <- mean(Y[, j], na.rm = TRUE); sg <- sd(Y[, j], na.rm = TRUE); na <- is.na(Y[, j])
    Y[na, j] <- rnorm(sum(na), mu - 1.8 * sg, 0.3 * sg) }
  p <- apply(Y, 1, function(r) t.test(r[cond == 'Treatment'], r[cond == 'Control'])$p.value)
  lfc <- rowMeans(Y[, cond == 'Treatment']) - rowMeans(Y[, cond == 'Control'])
  truth_eval(rownames(Y)[p < 0.05 & abs(lfc) > 1], truth, sprintf('seed %d downshift, p<0.05 & |log2FC|>1', s))
  truth_eval(rownames(Y)[p < 0.05], truth, sprintf('seed %d downshift, raw p<0.05 alone', s))
}
cat('--- Skill route: limma block + treat(lfc = 1) ---\n')
protein_matrix <- X
run_block('b01')
truth_eval(rownames(results)[results$adj.P.Val < 0.05], truth, 'Skill limma BH<0.05 (H0: FC = 0)')
dbl <- rownames(results)[results$adj.P.Val < 0.05 & abs(results$logFC) > 1]
truth_eval(dbl, truth, 'limma BH<0.05 & |log2FC|>1 double filter')
src <- sub('LFC_THRESHOLD <- log2(1.2)', 'LFC_THRESHOLD <- 1', readLines(list.files(BLK, pattern = '^b02', full.names = TRUE)), fixed = TRUE)
tf <- tempfile(fileext = '.R'); writeLines(src, tf); sys.source(tf, envir = globalenv())
truth_eval(rownames(results)[results$adj.P.Val < 0.05], truth, 'Skill treat(lfc = 1, trend, robust) BH<0.05')
