# Input 8 (NEW -- not in pre-fix audit's 7 inputs) -- bio-causal-genomics-mediation-analysis
# Prompt: "I have observational data on a binary treatment (drug exposure), a continuous
# biomarker mediator, a continuous outcome, and several confounders. I don't trust that
# either the mediator model or the outcome model is correctly specified -- can you give
# me a doubly-robust double-ML mediation estimate (medDML) instead of the standard
# product-of-coefficients approach?"
#
# Following SKILL.md "Double-ML Doubly-Robust Mediation" pattern (causalweight::medDML).
# This method is NOT one of the 7 pre-fix audit inputs -- the pre-fix audit never executed
# medDML at all. It is chosen specifically because the candidate's own TOOLS.md flagged
# (Notes for auditors #1) that the Skill's OWN toy-scale example parameters (small n,
# unnamed covariate columns) crash inside hdm::rlassologit with a confusing, undocumented
# error -- SKILL.md's Common Errors table only documents "trim removes most data", not this
# failure mode. This input tests both scales to check whether that gap is real and whether
# the Skill gives the agent any way to recognize/recover from it.
# SYNTHETIC DATA (planted total/direct/indirect effects for ground truth).

library(causalweight)
cat("causalweight version:", as.character(packageVersion("causalweight")), "\n\n")

make_data <- function(n, seed) {
  set.seed(seed)
  age <- rnorm(n, 50, 10)
  sex <- rbinom(n, 1, 0.5)
  bmi <- rnorm(n, 27, 4)
  x <- data.frame(age = age, sex = sex, bmi = bmi)
  # Planted: treatment propensity depends on covariates
  treat <- rbinom(n, 1, plogis(-0.5 + 0.02 * age - 0.3 * sex + 0.03 * bmi))
  # Planted: mediator (biomarker) depends on treatment + covariates; a-path = 0.6
  mediator <- 0.6 * treat + 0.02 * age + 0.1 * bmi + rnorm(n, 0, 1)
  # Planted: outcome depends on mediator (b-path = 0.5) + direct treatment effect (c' = 0.25)
  outcome <- 0.5 * mediator + 0.25 * treat + 0.01 * age - 0.05 * sex + rnorm(n, 0, 1)
  list(y = outcome, d = treat, m = mediator, x = x)
}

cat("=== Part A: n=300, following SKILL.md's medDML code pattern literally\n")
cat("    (named covariate data.frame -> as.matrix(dat[, covariates])) ===\n")
dA <- make_data(300, 8001)
resA <- tryCatch({
  medDML(y = dA$y, d = dA$d, m = dA$m, x = as.matrix(dA$x), trim = 0.05, order = 1)
}, error = function(e) e)
if (inherits(resA, "error")) {
  cat("medDML FAILED at n=300:\n  ", conditionMessage(resA), "\n\n")
} else {
  cat("medDML succeeded at n=300. results matrix:\n")
  print(round(resA$results, 4))
  cat("\n")
}

cat("=== Part B: n=800, matching the audit-env's own verified smoke-test scale ===\n")
dB <- make_data(800, 8002)
resB <- tryCatch({
  medDML(y = dB$y, d = dB$d, m = dB$m, x = as.matrix(dB$x), trim = 0.05, order = 1)
}, error = function(e) e)
if (inherits(resB, "error")) {
  cat("medDML FAILED at n=800:\n  ", conditionMessage(resB), "\n\n")
} else {
  cat("medDML succeeded at n=800. results matrix:\n")
  print(round(resB$results, 4))
  cat("\nPlanted ground truth: a-path (treat->mediator)=0.6, b-path (mediator->outcome)=0.5,\n")
  cat("direct c'=0.25 -> approx indirect = a*b = 0.30, approx total = indirect + direct = 0.55\n")
}

cat("\n=== Part C: n=150, sparser/more collinear covariates -- probe the exact\n")
cat("    failure the audit-env's TOOLS.md flagged for the Skill's own toy example ===\n")
set.seed(8003)
n_small <- 150
age_s <- rnorm(n_small, 50, 10)
x_s <- cbind(age_s, age_s * 0.9 + rnorm(n_small, 0, 0.5))  # near-collinear, UNNAMED columns
d_s <- rbinom(n_small, 1, plogis(0.02 * age_s))
m_s <- 0.5 * d_s + 0.1 * age_s + rnorm(n_small)
y_s <- 0.4 * m_s + 0.2 * d_s + rnorm(n_small)
resC <- tryCatch({
  medDML(y = y_s, d = d_s, m = m_s, x = x_s, trim = 0.05, order = 1)
}, error = function(e) e)
if (inherits(resC, "error")) {
  cat("medDML FAILED at n=150 with unnamed/near-collinear covariates:\n  ", conditionMessage(resC), "\n")
  cat("This matches the audit-env TOOLS.md finding: SKILL.md's Common Errors table does NOT\n")
  cat("document this failure mode (only 'trim removes most data' is listed) -- see recommendation.\n")
} else {
  cat("medDML succeeded at n=150 (unnamed covariates). results matrix:\n")
  print(round(resC$results, 4))
}
