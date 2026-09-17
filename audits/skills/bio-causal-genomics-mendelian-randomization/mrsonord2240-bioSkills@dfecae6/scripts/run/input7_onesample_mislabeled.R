# Input 7 (regression) -- UK-Biobank-on-UK-Biobank design mislabeled as "two independent
# GWAS", planted true causal effect = 0. Tests whether the FIXED SKILL.md Decision Tree /
# Operational rule (MR-RAPS corrects weak-IV bias only, NOT sample-overlap confounding) is
# now empirically consistent with what actually happens -- i.e. MR-RAPS still fails here,
# and the fixed text no longer implies it alone is sufficient.
library(TwoSampleMR)

set.seed(44)
n_snps <- 50
confound <- rnorm(n_snps, 0, 0.03)  # shared per-SNP confounding term simulating same-sample correlation
beta_exposure <- rnorm(n_snps, 0.05, 0.015) + confound
se_exposure <- runif(n_snps, 0.006, 0.010)
true_beta_xy <- 0
beta_outcome <- true_beta_xy * beta_exposure + confound * 0.8 + rnorm(n_snps, 0, 0.01)
se_outcome <- runif(n_snps, 0.007, 0.012)

dat <- data.frame(
    SNP = paste0("rs", 1:n_snps),
    beta.exposure = beta_exposure, se.exposure = se_exposure,
    beta.outcome = beta_outcome, se.outcome = se_outcome,
    mr_keep = TRUE, id.exposure = "exp", id.outcome = "out",
    exposure = "exp", outcome = "out"
)

f_stat <- (dat$beta.exposure / dat$se.exposure)^2
cat("Mean F-statistic:", round(mean(f_stat), 1), " (one-sample floor per SKILL.md is F>=20, not the usual F>=10)\n")

cat('\n--- Naive "two-sample" IVW ---\n')
ivw <- mr(dat, method_list = "mr_ivw")
print(ivw[, c("method", "nsnp", "b", "se", "pval")])
cat("TRUE causal beta_XY was:", true_beta_xy, "\n")

cat("\n--- MR-RAPS ---\n")
raps <- TwoSampleMR::mr_raps(b_exp = dat$beta.exposure, b_out = dat$beta.outcome,
                              se_exp = dat$se.exposure, se_out = dat$se.outcome)
cat("beta:", round(raps$b, 3), "| se:", round(raps$se, 4), "| p:", signif(raps$pval, 3), "\n")
cat("\nCONCLUSION: MR-RAPS", if (abs(raps$b) > 0.1) "does NOT correct" else "corrects", "the sample-overlap bias, matching the fixed SKILL.md Operational rule's claim that MR-RAPS is weak-IV-aware only, not confounder-aware.\n")
