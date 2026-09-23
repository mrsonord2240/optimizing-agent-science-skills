set.seed(2026092303)
blocks <- factor(rep(sprintf("day%d", 1:6), each = 8))
treatment <- factor(rep(rep(c("ctrl", "treat"), each = 4), 6))
block_effect <- rep(rnorm(6, sd = 1.1), each = 8)
y <- 0.7 * (treatment == "treat") + block_effect + rnorm(48, sd = 0.45)
fit_blocked <- lm(y ~ treatment + blocks)
fit_unblocked <- lm(y ~ treatment)
coef_blocked <- coef(summary(fit_blocked))["treatmenttreat", ]
coef_unblocked <- coef(summary(fit_unblocked))["treatmenttreat", ]
stopifnot(coef_blocked["Std. Error"] < coef_unblocked["Std. Error"], coef_blocked["Pr(>|t|)"] < 0.05)
cat(sprintf("blocked_se=%.4f unblocked_se=%.4f blocked_p=%.6f\n", coef_blocked["Std. Error"], coef_unblocked["Std. Error"], coef_blocked["Pr(>|t|)"]))
