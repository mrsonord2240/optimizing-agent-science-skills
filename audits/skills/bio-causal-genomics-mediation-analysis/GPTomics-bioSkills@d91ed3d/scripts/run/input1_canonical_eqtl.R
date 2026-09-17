# Input 1 (Canonical) -- bio-causal-genomics-mediation-analysis audit
# Prompt: "I have individual-level data on genotype, gene expression, and binary
# disease status with covariates age/sex/PCs. Test whether expression mediates the
# genotype-disease association and report ACME with 95% CI and proportion mediated;
# include Imai sensitivity analysis."
#
# Following SKILL.md "Single-Mediator Observational with Sensitivity" pattern.
# Synthetic data generated here (labelled synthetic); planted mediation effect.

library(mediation)

set.seed(1001)
n <- 500

genotype <- rbinom(n, 2, 0.3)
age <- rnorm(n, 55, 10)
sex <- rbinom(n, 1, 0.5)
pc1 <- rnorm(n); pc2 <- rnorm(n); pc3 <- rnorm(n)

# Planted a-path: genotype -> expression, beta = 0.45
expression <- 0.45 * genotype + 0.01 * age - 0.08 * sex + 0.2 * pc1 + rnorm(n, 0, 0.8)

# Planted b-path: expression -> disease (log-odds 0.35); residual direct c' = 0.12
logit_p <- -2 + 0.35 * expression + 0.12 * genotype + 0.02 * age + 0.05 * sex
disease <- rbinom(n, 1, plogis(logit_p))

dat <- data.frame(genotype, expression, disease, age, sex, pc1, pc2, pc3)
write.csv(dat, "../data/input1_eqtl_synthetic.csv", row.names = FALSE)

cat("=== Input 1: Canonical single-mediator eQTL mediation (SYNTHETIC DATA) ===\n")
cat("n =", n, "; planted a-path (genotype->expression) = 0.45; planted b-path (expression->disease, logit) = 0.35\n\n")

med_model <- lm(expression ~ genotype + age + sex + pc1 + pc2 + pc3, data = dat)
out_model <- glm(disease ~ genotype + expression + age + sex + pc1 + pc2 + pc3,
                  data = dat, family = binomial)

cat("Mediator model coef (genotype->expression):", round(coef(med_model)["genotype"], 4),
    " p =", format.pval(summary(med_model)$coefficients["genotype", 4]), "\n")
cat("Outcome model coef (expression->disease):", round(coef(out_model)["expression"], 4), "\n\n")

med_result <- mediate(med_model, out_model,
                       treat = "genotype", mediator = "expression",
                       boot = TRUE, sims = 5000, boot.ci.type = "bca")

cat("--- mediate() results (sims=5000, BCa) ---\n")
cat("ACME:", round(med_result$d0, 4), " [", round(med_result$d0.ci[1], 4), ",",
    round(med_result$d0.ci[2], 4), "]  p =", format.pval(med_result$d0.p), "\n")
cat("ADE :", round(med_result$z0, 4), " [", round(med_result$z0.ci[1], 4), ",",
    round(med_result$z0.ci[2], 4), "]  p =", format.pval(med_result$z0.p), "\n")
cat("Total:", round(med_result$tau.coef, 4), " p =", format.pval(med_result$tau.p), "\n")
cat("Proportion mediated:", round(med_result$n0, 4), " p =", format.pval(med_result$n0.p), "\n\n")

# --- Sensitivity: medsens requires linear or probit outcome; refit with probit ---
out_probit <- glm(disease ~ genotype + expression + age + sex + pc1 + pc2 + pc3,
                   data = dat, family = binomial(link = "probit"))
med_probit <- mediate(med_model, out_probit, treat = "genotype", mediator = "expression",
                       boot = TRUE, sims = 1000)
sens <- medsens(med_probit, rho.by = 0.05, effect.type = "indirect", sims = 1000)
cat("--- Imai rho sensitivity (medsens, probit refit) ---\n")
s <- summary(sens)
print(s)

# Extract rho_crit programmatically
rho_grid <- sens$rho
acme_grid <- sens$d0
sign_change <- which(diff(sign(acme_grid)) != 0)
if (length(sign_change) > 0) {
  rho_crit <- rho_grid[sign_change[1]]
  cat("\nApprox rho_crit (ACME crosses 0):", round(rho_crit, 3), "\n")
  cat("Robustness:", ifelse(abs(rho_crit) > 0.3, "reasonably robust (>0.3)",
                       ifelse(abs(rho_crit) < 0.1, "highly sensitive (<0.1)", "moderate (0.1-0.3)")), "\n")
} else {
  cat("\nACME does not cross zero within rho in [-1,1]: sensitivity range not bounded by grid.\n")
}
