# Input 8 v2 -- retry with a much larger background variant set for est_cause_params
# (CAUSE's own warning at v1 said "fewer than 100,000 variants... not recommended"; testing
# whether the in_sample_elpd_loo crash at v1 was a genuine defect or a too-small-scale artifact).
library(cause)

set.seed(77)
n_total <- 30000
n_causal_iv <- 150
true_gamma <- 0.35

beta_hat_1 <- rnorm(n_total, 0, 0.01)
beta_hat_2 <- rnorm(n_total, 0, 0.01)
se1 <- rep(0.01, n_total)
se2 <- rep(0.01, n_total)

chp_idx <- sample(setdiff(1:n_total, 1:n_causal_iv), 80)
u_effect <- rnorm(length(chp_idx), 0, 0.05)
beta_hat_1[chp_idx] <- beta_hat_1[chp_idx] + u_effect
beta_hat_2[chp_idx] <- beta_hat_2[chp_idx] + u_effect * 0.6

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

set.seed(100)
varlist <- sample(X$snp, size = nrow(X), replace = FALSE)  # use ALL variants as background this time

cat("\n--- est_cause_params (n_iter=10, background = ALL", nrow(X), "variants) ---\n")
t0 <- Sys.time()
params <- est_cause_params(X, varlist, n_iter = 10)
cat("est_cause_params wall time (s):", round(as.numeric(Sys.time() - t0, units = "secs"), 1), "\n")
cat("rho:", round(params$rho, 4), "\n")

sig_snps <- X$snp[X$p1 < 1e-3]
cat("\nSig SNPs for cause() (P<1e-3):", length(sig_snps), "\n")

cat("\n--- cause() ---\n")
t1 <- Sys.time()
res <- tryCatch(cause(X = X, variants = sig_snps, param_ests = params),
                error = function(e) { cat("cause() ERROR:", conditionMessage(e), "\n"); NULL })
cat("cause() wall time (s):", round(as.numeric(Sys.time() - t1, units = "secs"), 1), "\n")

if (!is.null(res)) {
    cat("\n--- Model comparison (ELPD) ---\n")
    print(summary(res))
    print(res$elpd)
    cat("\nTrue causal gamma was:", true_gamma, "; planted CHP via", length(chp_idx), "shared-confounder SNPs\n")
} else {
    cat("\ncause() crashed even with", nrow(X), "background variants -- see error above.\n")
}
