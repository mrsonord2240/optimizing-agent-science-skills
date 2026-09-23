set.seed(2026092304)
library(lme4)
library(lmerTest)
df <- expand.grid(run = factor(sprintf("lane%d", 1:5)), sample = 1:4, KEEP.OUT.ATTRS = FALSE)
df$genotype <- factor(rep(c("WT", "WT", "KO", "KO"), 5))
df$run_effect <- rnorm(5, sd = 1.2)[df$run]
df$expression <- 0.9 * (df$genotype == "KO") + df$run_effect + rnorm(nrow(df), sd = 0.4)
flat <- lm(expression ~ genotype, data = df)
mixed <- lmer(expression ~ genotype + (1 | run), data = df)
flat_se <- coef(summary(flat))["genotypeWT", "Std. Error"]
mixed_se <- coef(summary(mixed))["genotypeWT", "Std. Error"]
run_var <- as.data.frame(VarCorr(mixed))$vcov[1]
stopifnot(is.finite(mixed_se), run_var > 0)
cat(sprintf("flat_se=%.4f mixed_se=%.4f run_variance=%.4f\n", flat_se, mixed_se, run_var))
