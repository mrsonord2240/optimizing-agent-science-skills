# Input 3 (regression): heavy MNAR missingness, on/off proteins, "don't impute". SYNTHETIC data.
source('F:/OpenScience/audits/bio-proteomics-differential-abundance/rerun/common.R')
suppressPackageStartupMessages(library(proDA))
truth <- read.csv(file.path(RR, 'data', 'truth_proteins.csv'))
mq <- load_maxquant_lfq()
sample_info <- read.csv(file.path(RR, 'data', 'sample_annotation.csv'))
sample_info$condition <- factor(sample_info$condition, levels = c('Control', 'Treatment'))
X <- mq$matrix[, sample_info$sample]
X <- X[rowSums(!is.na(X)) > 0, ]          # proteins with no value at all carry no information
protein_matrix <- X
cond <- sample_info$condition
absT <- rownames(X)[rowSums(!is.na(X[, cond == 'Treatment'])) == 0]
cat('rows:', nrow(X), '| absent in all Treatment:', length(absT), '| missing %:', round(100 * mean(is.na(X)), 1), '\n')

set.seed(1)
run_block('b04')   # proDA block verbatim: ~condition + batch, reference_level Control, test_diff 'conditionTreatment'
print(result_names(fit))
sig <- results$name[results$adj_pval < 0.05]
truth_eval(sig, truth, 'proDA ~condition+batch adj_pval<0.05')
ao <- results[results$name %in% absT, ]
ac <- truth$class[match(ao$name, truth$protein)]
cat('absent-in-T proteins: diff range', round(range(ao$diff), 2), '| min adj_pval', signif(min(ao$adj_pval), 2),
    '| median diff for null', round(median(ao$diff[ac == 'null']), 2), '| for on_off', round(median(ao$diff[ac == 'on_off']), 2), '\n')

# Downshift (Perseus 1.8/0.3) + limma comparison, 5 seeds -- to check the Skill's revised claims
cat('--- downshift + limma, 5 seeds ---\n')
Xf <- X[apply(sapply(levels(cond), function(g) rowSums(!is.na(X[, cond == g, drop = FALSE]))) >= 3, 1, any), ]
for (s in 1:5) {
  set.seed(s); Y <- Xf
  for (j in seq_len(ncol(Y))) { mu <- mean(Y[, j], na.rm = TRUE); sg <- sd(Y[, j], na.rm = TRUE); na <- is.na(Y[, j])
    Y[na, j] <- rnorm(sum(na), mu - 1.8 * sg, 0.3 * sg) }
  d <- model.matrix(~0 + condition + batch, data = sample_info); colnames(d)[1:2] <- levels(cond)
  f <- eBayes(contrasts.fit(lmFit(Y, d), makeContrasts(Treatment - Control, levels = d)), trend = TRUE, robust = TRUE)
  tt <- topTable(f, number = Inf)
  truth_eval(rownames(tt)[tt$adj.P.Val < 0.05], truth, sprintf('downshift seed %d + limma BH<0.05', s))
  if (s == 1) {
    one <- intersect(rownames(Y), absT)
    cat('  wing: cor(logFC, AveExpr) among absent-in-T:', round(cor(tt[one, 'logFC'], tt[one, 'AveExpr']), 2),
        '| median sd per run used for imputation SD:', round(0.3 * median(apply(Xf, 2, sd, na.rm = TRUE)), 2),
        '| median real replicate SD:', round(median(apply(Xf[complete.cases(Xf), cond == 'Control'], 1, sd)), 2), '\n')
  }
}
