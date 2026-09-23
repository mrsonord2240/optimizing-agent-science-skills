# REGRESSION of pre-fix audit Input 3 (Edge) -- LD reference mismatch diagnostic
# (estimate_s_rss / kriging_rss). Unchanged code path from the pre-fix audit -- pure regression.
suppressMessages(library(susieR))

set.seed(303)
n_samples <- 5000
n_snps <- 300
planted_causal <- 150
planted_beta <- 1.1

simulate_X <- function(n_samples, n_snps, window, seed) {
  set.seed(seed)
  X <- matrix(0, n_samples, n_snps)
  i <- 1
  while (i <= n_snps) {
    end <- min(n_snps, i + window - 1)
    latent <- rnorm(n_samples)
    for (j in i:end) {
      maf <- runif(1, 0.15, 0.4)
      liab <- 0.8 * latent + sqrt(1 - 0.8^2) * rnorm(n_samples)
      thresh <- quantile(liab, 1 - maf)
      X[, j] <- rbinom(n_samples, 2, pmin(pmax(plogis((liab - thresh) * 2 + qlogis(maf)), 0.01), 0.99))
    }
    i <- end + 1
  }
  scale(X)
}

X_A <- simulate_X(n_samples, n_snps, window = 10, seed = 303)
y_A <- X_A[, planted_causal] * planted_beta + rnorm(n_samples, 0, 3)
r_vec <- as.numeric(cor(X_A, y_A))
z_scores <- r_vec * sqrt((n_samples - 2) / (1 - r_vec^2))
true_ld <- cor(X_A)

X_B <- simulate_X(n_samples, n_snps, window = 25, seed = 909)
mismatched_ld <- cor(X_B)

cat('=== Diagnostic with the (deliberately) mismatched reference LD ===\n')
s_hat_bad <- estimate_s_rss(z = z_scores, R = mismatched_ld, n = n_samples)
cat(sprintf('estimate_s_rss lambda (mismatched ref) = %.4f\n', s_hat_bad))
cond_z_bad <- kriging_rss(z = z_scores, R = mismatched_ld, n = n_samples)
flag_bad <- sum(abs(cond_z_bad$conditional_dist$z_std_diff) > 3)
cat(sprintf('kriging_rss flagged %d / %d SNPs (mismatched ref)\n', flag_bad, n_snps))

cat('\n=== Same z-scores against the correctly matched (in-sample) LD, for comparison ===\n')
s_hat_good <- estimate_s_rss(z = z_scores, R = true_ld, n = n_samples)
cond_z_good <- kriging_rss(z = z_scores, R = true_ld, n = n_samples)
flag_good <- sum(abs(cond_z_good$conditional_dist$z_std_diff) > 3)
cat(sprintf('estimate_s_rss lambda (matched ref)    = %.4f\n', s_hat_good))
cat(sprintf('kriging_rss flagged %d / %d SNPs (matched ref)\n', flag_good, n_snps))

cat('\n=== susie_rss fit using the mismatched reference (what would be wrongly reported) ===\n')
fit_bad <- susie_rss(z = z_scores, R = mismatched_ld, n = n_samples, L = 10, estimate_residual_variance = TRUE)
cat(sprintf('Credible sets on mismatched LD: %d\n', length(fit_bad$sets$cs)))
if (length(fit_bad$sets$cs) > 0) {
  sizes <- sapply(fit_bad$sets$cs, length)
  cat('CS sizes:', paste(sizes, collapse=', '), '\n')
}

cat('\nASSERT lambda(mismatched) > lambda(matched):', s_hat_bad > s_hat_good, '\n')
cat('ASSERT lambda(mismatched) exceeds the Skill\'s 0.05 acceptable threshold:', s_hat_bad > 0.05, '\n')
cat('ASSERT lambda(matched) is within the Skill\'s acceptable range:', s_hat_good < 0.05, '\n')
cat('ASSERT kriging_rss flags more (or equal) outliers under mismatch:', flag_bad >= flag_good, '\n')
