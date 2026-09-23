# Input 4 (Variant B) -- bio-causal-genomics-mediation-analysis audit
# Prompt: "Use MVMR-mediation to estimate the direct effect of LDL on CHD adjusting
# for HDL; report conditional F for each exposure and the indirect path through HDL."
#
# Following SKILL.md "MR-Mediation: Total Minus Direct via MVMR" pattern.
# OpenGWAS is gated (401 without a token, confirmed in TOOLS.md) so this uses
# SIMULATED SNP-level summary statistics with a planted mediated structure,
# exactly as the Skill's own mvmr_mediation.R example does -- labelled synthetic.

library(TwoSampleMR)
library(MVMR)

set.seed(4004)
n_snps <- 90

beta_E <- rnorm(n_snps, 0, 0.05)                    # SNP -> LDL (E)
beta_M <- 0.35 * beta_E + rnorm(n_snps, 0, 0.03)     # SNP -> HDL (M), partly via LDL
se_E <- abs(rnorm(n_snps, 0.01, 0.002))
se_M <- abs(rnorm(n_snps, 0.01, 0.002))

# Planted: direct LDL->CHD = 0.10; HDL->CHD = -0.6 (protective); total should be
# direct + 0.35*(-0.6) path contribution approx
beta_Y <- 0.10 * beta_E + (-0.6) * beta_M + rnorm(n_snps, 0, 0.005)
se_Y <- abs(rnorm(n_snps, 0.005, 0.001))

snps <- paste0("rs", sprintf("%06d", sample(1e6, n_snps)))

harm_total <- data.frame(
  SNP = snps,
  beta.exposure = beta_E, se.exposure = se_E,
  beta.outcome = beta_Y, se.outcome = se_Y,
  effect_allele.exposure = "A", other_allele.exposure = "G",
  effect_allele.outcome = "A", other_allele.outcome = "G",
  eaf.exposure = runif(n_snps, 0.1, 0.5),
  eaf.outcome = runif(n_snps, 0.1, 0.5),
  exposure = "LDL", outcome = "CHD", id.exposure = "LDL", id.outcome = "CHD",
  mr_keep = TRUE,
  pval.exposure = runif(n_snps, 1e-12, 1e-7),
  pval.outcome = runif(n_snps, 1e-3, 0.5)
)
write.csv(data.frame(SNP = snps, beta_E, se_E, beta_M, se_M, beta_Y, se_Y),
          "../data/input4_mvmr_synthetic_sumstats.csv", row.names = FALSE)

cat("=== Input 4: MVMR-mediation, LDL->CHD via HDL (SYNTHETIC SUMMARY STATS) ===\n")
cat("Planted: direct LDL->CHD=0.10; HDL->CHD=-0.6; LDL->HDL path=0.35\n\n")

total <- mr_ivw(b_exp = harm_total$beta.exposure, b_out = harm_total$beta.outcome,
                 se_exp = harm_total$se.exposure, se_out = harm_total$se.outcome)
cat("--- Univariable MR (Total Effect LDL -> CHD) ---\n")
cat("Total beta:", round(total$b, 4), " SE:", round(total$se, 4),
    " p:", format.pval(total$pval), "\n")

mvmr_dat <- format_mvmr(BXGs = cbind(beta_E, beta_M),
                         BYG = beta_Y, seBXGs = cbind(se_E, se_M), seBYG = se_Y, RSID = snps)

fstat <- strength_mvmr(mvmr_dat, gencov = 0)
cat("\n--- Conditional F-statistics (require > 10 per exposure) ---\n")
print(fstat)

qstat <- pleiotropy_mvmr(mvmr_dat, gencov = 0)
cat("\n--- MVMR Q-statistic for instrument heterogeneity ---\n")
print(qstat)

mvmr_fit <- ivw_mvmr(mvmr_dat)
cat("\n--- MVMR (Direct Effects) ---\n")
print(mvmr_fit)

direct_E <- mvmr_fit[1, "Estimate"]
direct_E_se <- mvmr_fit[1, "Std. Error"]

indirect <- total$b - direct_E
indirect_se <- sqrt(total$se^2 + direct_E_se^2)
indirect_ci <- indirect + c(-1.96, 1.96) * indirect_se
prop_med <- indirect / total$b

cat("\n--- Indirect Effect (Total - Direct), i.e. via HDL ---\n")
cat("Indirect:", round(indirect, 4), " SE:", round(indirect_se, 4), "\n")
cat("95% CI: [", round(indirect_ci[1], 4), ",", round(indirect_ci[2], 4), "]\n")
cat("Proportion mediated:", round(prop_med, 3), "\n\n")

if (any(fstat < 10)) {
  cat("WARNING: conditional F < 10 detected. Weak-instrument bias possible.\n")
} else {
  cat("Conditional F check: both exposures pass F > 10 (per Sanderson 2019 / Skill's own threshold table).\n")
}
if (qstat$Qpval < 0.05) {
  cat("Q-statistic p <0.05: substantial pleiotropy -- indirect estimate should be treated as exploratory.\n")
} else {
  cat("Q-statistic not significant: no strong evidence against instrument validity from this diagnostic.\n")
}
cat("Direct/Total sign check:", ifelse(sign(direct_E) == sign(total$b), "consistent", "SIGN FLIP -- investigate"), "\n")
