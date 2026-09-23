# Input 8 (NEW -- CAUSE is now installed in this env, was absent pre-fix). Tests SKILL.md's
# "CAUSE for Correlated Horizontal Pleiotropy" section end to end: gwas_merge() -> sample for
# est_cause_params() -> filter sig SNPs -> cause(). Synthetic genome-wide-scale data (5000
# variants) with a planted CAUSAL effect PLUS correlated horizontal pleiotropy (CHP) via a
# shared confounder factor -- the scenario CAUSE exists to distinguish from pure causation.
# Reduced n_iter (10, not default 20) for tractable runtime per the audit brief's timing note.
library(cause)

set.seed(77)
n_total <- 5000
n_causal_iv <- 150      # genuine cis/trans instruments for X, >=100 per SKILL.md's floor
true_gamma <- 0.35       # true causal effect X -> Y

# Background: most SNPs null in both traits (LD-score-like noise floor)
beta_hat_1 <- rnorm(n_total, 0, 0.01)
beta_hat_2 <- rnorm(n_total, 0, 0.01)
se1 <- rep(0.01, n_total)
se2 <- rep(0.01, n_total)

# Confounder pathway: a shared factor U affects a DISTINCT set of SNPs in both traits directly
# (correlated horizontal pleiotropy), independent of the causal SNPs below.
chp_idx <- sample(setdiff(1:n_total, 1:n_causal_iv), 80)
u_effect <- rnorm(length(chp_idx), 0, 0.05)
beta_hat_1[chp_idx] <- beta_hat_1[chp_idx] + u_effect
beta_hat_2[chp_idx] <- beta_hat_2[chp_idx] + u_effect * 0.6  # correlated but not identical scaling

# Causal instruments: real genome-wide-significant effect on X, propagates to Y via true_gamma
snp_effect_x <- rnorm(n_causal_iv, 0, 0.06)
beta_hat_1[1:n_causal_iv] <- snp_effect_x
beta_hat_2[1:n_causal_iv] <- snp_effect_x * true_gamma + rnorm(n_causal_iv, 0, 0.01)

X <- data.frame(
    snp = paste0("rs", 1:n_total),
    beta_hat_1 = beta_hat_1, seb1 = se1,
    beta_hat_2 = beta_hat_2, seb2 = se2,
    p1 = 2 * pnorm(-abs(beta_hat_1 / se1)),
    p2 = 2 * pnorm(-abs(beta_hat_2 / se2))
)
cat("Total variants:", nrow(X), "\n")
cat("Genome-wide-sig on trait 1 (p<5e-8):", sum(X$p1 < 5e-8), "\n")

set.seed(100)
varlist <- sample(X$snp, size = min(2000, nrow(X)), replace = FALSE)

cat("\n--- est_cause_params (nuisance parameters, n_iter=10, reduced for tractability) ---\n")
t0 <- Sys.time()
params <- est_cause_params(X, varlist, n_iter = 10)
cat("est_cause_params wall time (s):", round(as.numeric(Sys.time() - t0, units = "secs"), 1), "\n")
cat("rho (correlation of null effects, proxy for confounding/overlap):", round(params$rho, 4), "\n")

sig_snps <- X$snp[X$p1 < 1e-3]
cat("\nSig SNPs for cause() (P<1e-3):", length(sig_snps), "(SKILL.md floor: >=100)\n")

cat("\n--- cause() ---\n")
t1 <- Sys.time()
res <- cause(X = X, variants = sig_snps, param_ests = params)
cat("cause() wall time (s):", round(as.numeric(Sys.time() - t1, units = "secs"), 1), "\n")

cat("\n--- Model comparison (ELPD) ---\n")
print(summary(res))
elpd <- res$elpd
print(elpd)
cat("\nCausal-vs-sharing delta ELPD z-score (row 'sharing vs causal'):\n")
print(elpd[elpd$model1 == "sharing" & elpd$model2 == "causal", ])
cat("\nTrue causal gamma was:", true_gamma, "; planted CHP via", length(chp_idx), "shared-confounder SNPs\n")
