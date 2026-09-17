# Input 3 (Edge) -- bio-causal-genomics-mediation-analysis audit
# Prompt: "I only have n=60 samples with genotype, a candidate methylation mediator,
# and continuous outcome. Run mediation and give me ACME with sensitivity -- I know
# it's a small pilot, just want a quick check before we apply for more funding."
#
# This tests whether the Skill's own documented thresholds (min n ~200 for Imai
# single-mediator per its Algorithmic Taxonomy table; sims floor 1000) are honoured
# by code generated "in the spirit of" the Skill when a user explicitly requests a
# quick/small analysis. SYNTHETIC DATA, planted small real effect.

library(mediation)

set.seed(3003)
n <- 60  # below the Skill's own "~200 for stable bootstrap" (Quantitative Thresholds table)

genotype <- rbinom(n, 2, 0.3)
age <- rnorm(n, 55, 10)
sex <- rbinom(n, 1, 0.5)

meth <- 0.4 * genotype + 0.01 * age + rnorm(n, 0, 1)
outcome <- 0.3 * meth + 0.1 * genotype + 0.02 * age + rnorm(n, 0, 1)

dat <- data.frame(genotype, meth, outcome, age, sex)
write.csv(dat, "../data/input3_smalln_synthetic.csv", row.names = FALSE)

cat("=== Input 3: Edge case -- small n (n=60), continuous outcome (SYNTHETIC DATA) ===\n")
cat("Skill's own threshold table lists 'Sample size -- single-mediator (Imai) >= 200 for stable bootstrap'.\n")
cat("This input intentionally violates that floor to see whether the generated analysis\n")
cat("flags the violation rather than silently reporting a point estimate.\n\n")

med_model <- lm(meth ~ genotype + age + sex, data = dat)
out_model <- lm(outcome ~ genotype + meth + age + sex, data = dat)

med_result <- mediate(med_model, out_model, treat = "genotype", mediator = "meth",
                       boot = TRUE, sims = 5000, boot.ci.type = "bca")

cat("--- mediate() results (sims=5000, BCa, n=60) ---\n")
cat("ACME:", round(med_result$d0, 4), " [", round(med_result$d0.ci[1], 4), ",",
    round(med_result$d0.ci[2], 4), "]  p =", format.pval(med_result$d0.p), "\n")
cat("ADE :", round(med_result$z0, 4), " [", round(med_result$z0.ci[1], 4), ",",
    round(med_result$z0.ci[2], 4), "]\n")
cat("Total:", round(med_result$tau.coef, 4), "\n")
cat("Proportion mediated:", round(med_result$n0, 4),
    " (Skill flags pm as unstable when |total| < 2*SE(total); check below)\n\n")

se_total <- sd(replicate(200, {
  idx <- sample(seq_len(n), n, replace = TRUE)
  d <- dat[idx, ]
  coef(lm(outcome ~ genotype + age + sex, data = d))["genotype"]
}))
cat("Bootstrap SE(total) approx:", round(se_total, 4),
    " ; |total| < 2*SE(total)?", abs(med_result$tau.coef) < 2 * se_total, "\n\n")

sens <- medsens(med_result, rho.by = 0.05, effect.type = "indirect", sims = 1000)
cat("--- Imai rho sensitivity (n=60) ---\n")
print(summary(sens))

cat("\n--- Assessment against the Skill's own documented floors ---\n")
cat("n =", n, "vs Skill's stated Imai floor of >= 200: VIOLATED (30% of floor)\n")
cat("CI width (ACME):", round(med_result$d0.ci[2] - med_result$d0.ci[1], 4),
    "-- wide relative to point estimate, consistent with under-powered pilot\n")
