# Audit input 4 (Edge) -- bio-metabolomics-statistical-analysis
# User request: "My cohort has 4 repeated timepoints per subject (longitudinal
# design). Fit a linear mixed model per metabolite testing the time effect,
# adjusting for BMI, and give me BH-FDR-corrected results."
#
# Synthetic longitudinal data: 20 subjects x 4 timepoints = 80 observations,
# 50 metabolites, 10 with a true time trend, subject-level random intercepts,
# and a BMI covariate that is a real confounder for a subset of features.
suppressMessages(library(lme4))
suppressMessages(library(lmerTest))

set.seed(11)
n_subj <- 20
n_time <- 4
n_features <- 50
n_true_time <- 10
n_true_bmi <- 8

subj <- rep(paste0('subj', 1:n_subj), each = n_time)
time <- rep(0:(n_time - 1), times = n_subj)
bmi <- rep(rnorm(n_subj, mean = 26, sd = 4), each = n_time)   # time-invariant covariate per subject
subj_re <- rep(rnorm(n_subj, sd = 0.8), each = n_time)         # random intercept per subject

meta <- data.frame(subj = subj, time = time, bmi = bmi)

res <- data.frame(feature = character(), beta_time = numeric(), p_time = numeric(),
                   beta_bmi = numeric(), p_bmi = numeric(), stringsAsFactors = FALSE)

for (f in seq_len(n_features)) {
    true_time_effect <- if (f <= n_true_time) 0.35 else 0
    true_bmi_effect <- if (f > n_true_time & f <= n_true_time + n_true_bmi) 0.05 else 0
    y <- 10 + true_time_effect * time + true_bmi_effect * bmi + subj_re + rnorm(n_subj * n_time, sd = 0.5)
    d <- cbind(meta, y = y)
    fit <- lmer(y ~ time + bmi + (1 | subj), data = d, REML = FALSE)
    s <- summary(fit)$coefficients
    res <- rbind(res, data.frame(
        feature = paste0('M', f),
        beta_time = s['time', 'Estimate'], p_time = s['time', 'Pr(>|t|)'],
        beta_bmi = s['bmi', 'Estimate'], p_bmi = s['bmi', 'Pr(>|t|)']
    ))
}

res$padj_time <- p.adjust(res$p_time, method = 'BH')   # explicit BH, per Skill guidance (R default is Holm)
res$padj_bmi <- p.adjust(res$p_bmi, method = 'BH')

hits_time <- res$feature[res$padj_time < 0.05]
true_time_features <- paste0('M', seq_len(n_true_time))
tp_time <- length(intersect(hits_time, true_time_features))
fp_time <- length(setdiff(hits_time, true_time_features))

cat(sprintf('Time-effect hits (BH padj<0.05): %d of %d features\n', length(hits_time), n_features))
cat(sprintf('True time-effect features recovered: %d of %d\n', tp_time, n_true_time))
cat(sprintf('False positives among time hits: %d\n', fp_time))
cat('\nTop 10 by padj_time:\n')
print(head(res[order(res$padj_time), c('feature', 'beta_time', 'p_time', 'padj_time')], 10))
