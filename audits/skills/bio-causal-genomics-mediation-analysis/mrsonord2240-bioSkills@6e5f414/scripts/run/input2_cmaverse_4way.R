# Input 2 (Variant A) -- bio-causal-genomics-mediation-analysis audit
# Prompt: "Decompose the smoking-COPD effect into CDE, PIE, INTref, INTmed using FEV1
# as the mediator and CMAverse; outcome is binary with rare-disease prevalence around
# 5-12%. Genotype substitutes for 'smoking' here (genomic mediation framing)."
#
# Following SKILL.md "4-Way Decomposition with Exposure-Mediator Interaction" pattern.
# Synthetic data generated here (labelled synthetic); planted E-M interaction.

library(CMAverse)
library(mediation)
library(EValue)

set.seed(2002)
n <- 1500

genotype <- rbinom(n, 2, 0.3)
age <- as.numeric(scale(rnorm(n, 55, 10)))
sex <- rbinom(n, 1, 0.5)
pc1 <- rnorm(n); pc2 <- rnorm(n)

expression <- 0.5 * genotype + 0.05 * age - 0.1 * sex + 0.2 * pc1 + rnorm(n, 0, 0.8)

# Planted: direct 0.15, mediator 0.3, E*M interaction 0.25
logit_p <- -2.5 + 0.15 * genotype + 0.3 * expression +
  0.25 * genotype * expression + 0.04 * age + 0.1 * sex + 0.1 * pc1
disease <- rbinom(n, 1, plogis(logit_p))

dat <- data.frame(genotype, expression, disease, age, sex, pc1, pc2)
write.csv(dat, "../data/input2_cmaverse_synthetic.csv", row.names = FALSE)

cat("=== Input 2: 4-way CMAverse decomposition (SYNTHETIC DATA) ===\n")
cat("n =", n, "; outcome prevalence:", round(mean(dat$disease), 3), "\n")
cat("Planted: direct=0.15, mediator=0.3, E*M interaction=0.25 (log-odds)\n\n")

result_4way <- cmest(
  data = dat, model = "rb",
  outcome = "disease", exposure = "genotype", mediator = "expression",
  basec = c("age", "sex", "pc1", "pc2"),
  EMint = TRUE,
  mreg = list("linear"), yreg = "logistic",
  astar = 0, a = 1, mval = list(0),
  estimation = "paramfunc", inference = "bootstrap", nboot = 1000,
  boot.ci.type = "per"
)

cat("--- 4-Way Decomposition (summary) ---\n")
s4 <- summary(result_4way)
print(s4)

cat("\n--- Column names actually returned (verify against SKILL.md claims) ---\n")
print(names(s4$summarydf))
print(rownames(s4$summarydf))

# --- Compare to standard (no-interaction) mediation, per Skill's stated pitfall ---
med_simple <- lm(expression ~ genotype + age + sex + pc1 + pc2, data = dat)
out_simple <- glm(disease ~ genotype + expression + age + sex + pc1 + pc2,
                   data = dat, family = binomial)
med_imai <- mediate(med_simple, out_simple, treat = "genotype", mediator = "expression",
                     boot = TRUE, sims = 1000)
cat("\n--- Standard (no-interaction) mediation for comparison ---\n")
cat("ACME:", round(med_imai$d0, 4), " [", round(med_imai$d0.ci[1], 4), ",",
    round(med_imai$d0.ci[2], 4), "]\n")
cat("ADE :", round(med_imai$z0, 4), " [", round(med_imai$z0.ci[1], 4), ",",
    round(med_imai$z0.ci[2], 4), "]\n")
cat("Total:", round(med_imai$tau.coef, 4), "\n")

# --- Mediational E-value on the no-interaction ACME, as SKILL.md illustrates ---
acme_rr <- exp(med_imai$d0)
acme_lower_rr <- exp(med_imai$d0.ci[1])
acme_upper_rr <- exp(med_imai$d0.ci[2])
cat("\n--- Mediational E-value (on the no-interaction ACME; illustrative, since\n")
cat("    the real quantity of interest here is the 4-way components above) ---\n")
print(evalues.RR(est = acme_rr, lo = acme_lower_rr, hi = acme_upper_rr))
