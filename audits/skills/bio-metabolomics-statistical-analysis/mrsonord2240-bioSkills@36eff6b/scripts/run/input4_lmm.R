# Regression test for pre-fix Input 4 (Edge): per-metabolite LMM, 4-timepoint longitudinal
# design, adjusting for BMI, BH FDR.
library(lme4)
library(lmerTest)

set.seed(555)
n_subj <- 20
n_time <- 4
n_feat <- 50
n_true_time <- 10
n_bmi_only <- 8

subj <- rep(seq_len(n_subj), each = n_time)
time <- rep(seq_len(n_time), times = n_subj)
bmi <- rep(rnorm(n_subj, mean = 26, sd = 3), each = n_time)
subj_re <- rep(rnorm(n_subj, sd = 0.5), each = n_time)

Y <- matrix(rnorm(n_subj * n_time * n_feat, mean = 10, sd = 1), nrow = n_subj * n_time, ncol = n_feat)
colnames(Y) <- paste0('M', seq_len(n_feat))
for (f in seq_len(n_true_time)) Y[, f] <- Y[, f] + 0.35 * time + subj_re
for (f in (n_true_time + 1):(n_true_time + n_bmi_only)) Y[, f] <- Y[, f] + 0.15 * (bmi - 26) + subj_re

pvals <- numeric(n_feat)
for (f in seq_len(n_feat)) {
    d <- data.frame(y = Y[, f], time = time, bmi = bmi, subj = factor(subj))
    m <- lmer(y ~ time + bmi + (1 | subj), data = d)
    pvals[f] <- summary(m)$coefficients['time', 'Pr(>|t|)']
}
padj <- p.adjust(pvals, method = 'BH')
hits <- which(padj < 0.05)
true_time <- seq_len(n_true_time)

cat('Time-effect hits (BH padj<0.05):', length(hits), 'of', n_feat, 'features\n')
cat('True time-effect features recovered:', length(intersect(hits, true_time)), 'of', n_true_time, '\n')
cat('False positives among time hits:', length(setdiff(hits, true_time)), '\n')
