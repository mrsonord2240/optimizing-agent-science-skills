# REGRESSION of pre-fix audit Input 5 (Stress) -- HLA-like non-sparse locus, 12 planted causals
# vs L=10 default cap. Unchanged code path from the pre-fix audit -- pure regression.
suppressMessages(library(susieR))

set.seed(505)
n_samples <- 8000
n_snps <- 500
n_true_causal <- 12
planted_causal <- sort(sample(seq(20, n_snps - 20, by = 38), n_true_causal))
planted_beta <- runif(n_true_causal, 0.5, 0.9) * sample(c(-1, 1), n_true_causal, replace = TRUE)

simulate_X <- function(n_samples, n_snps, window, seed) {
  set.seed(seed)
  X <- matrix(0, n_samples, n_snps)
  i <- 1
  while (i <= n_snps) {
    end <- min(n_snps, i + window - 1)
    latent <- rnorm(n_samples)
    for (j in i:end) {
      maf <- runif(1, 0.15, 0.4)
      liab <- 0.7 * latent + sqrt(1 - 0.7^2) * rnorm(n_samples)
      thresh <- quantile(liab, 1 - maf)
      X[, j] <- rbinom(n_samples, 2, pmin(pmax(plogis((liab - thresh) * 2 + qlogis(maf)), 0.01), 0.99))
    }
    i <- end + 1
  }
  scale(X)
}

X <- simulate_X(n_samples, n_snps, window = 6, seed = 505)
y <- X[, planted_causal] %*% planted_beta + rnorm(n_samples, 0, 4)
y <- as.numeric(y)

ld_matrix <- cor(X)
r_vec <- as.numeric(cor(X, y))
z_scores <- r_vec * sqrt((n_samples - 2) / (1 - r_vec^2))

cat('=== L=10 (default) ===\n')
fit10 <- susie_rss(z = z_scores, R = ld_matrix, n = n_samples, L = 10, estimate_residual_variance = TRUE)
cat(sprintf('Credible sets returned: %d (== requested L? %s)\n',
            length(fit10$sets$cs), length(fit10$sets$cs) == 10))

cat('\n=== L=30 (raised per Skill guidance for HLA / >5-signal loci) ===\n')
fit30 <- susie_rss(z = z_scores, R = ld_matrix, n = n_samples, L = 30, estimate_residual_variance = TRUE)
cat(sprintf('Credible sets returned: %d / 30 requested (auto-pruned? %s)\n',
            length(fit30$sets$cs), length(fit30$sets$cs) < 30))

captured10 <- sum(sapply(planted_causal, function(c) any(sapply(fit10$sets$cs, function(cs) c %in% cs))))
captured30 <- sum(sapply(planted_causal, function(c) any(sapply(fit30$sets$cs, function(cs) c %in% cs))))
cat(sprintf('\nPlanted causals (of %d) captured at L=10: %d\n', n_true_causal, captured10))
cat(sprintf('Planted causals (of %d) captured at L=30: %d\n', n_true_causal, captured30))

cat('\nASSERT L=10 saturates all requested slots (signal that L is undersized):',
    length(fit10$sets$cs) == 10, '\n')
cat('ASSERT L=30 returns fewer than the 30 cap (auto-pruning, per Skill):',
    length(fit30$sets$cs) < 30, '\n')
cat('ASSERT raising L recovers at least as many planted causals as L=10:',
    captured30 >= captured10, '\n')
