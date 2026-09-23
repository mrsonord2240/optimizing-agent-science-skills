# REGRESSION of pre-fix audit Input 1 (Canonical) -- "Fine-map a 1 Mb window around a lead SNP
# using susie_rss with a matched LD reference. Run estimate_s_rss and report lambda. Extract 95%
# credible sets, purity, and top PIP variants." (SKILL.md's own worked example / usage-guide.md
# "Single-Locus EUR GWAS" prompt.) Re-run unchanged from the pre-fix audit against the fixed Skill
# (fix/cg-fine-mapping @ c5fd9ff) -- this code path was not touched by the fix, so it is a pure
# regression check that susieR 0.14.2 + coloc 5.2.3 in this env still reproduce the pre-fix result.
suppressMessages(library(susieR))

set.seed(101)
n_samples <- 6000
n_snps <- 400
planted_causal <- c(90, 310)

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

X <- simulate_X(n_samples, n_snps, window = 10, seed = 101)
beta <- rep(0, n_snps); beta[planted_causal] <- c(0.9, 0.75)
y <- X %*% beta + rnorm(n_samples, 0, 3)
y <- as.numeric(y)

# GWAS z-scores AND the LD reference both derive from the same simulated genotype matrix --
# a genuinely matched reference (unlike a hand-written banded correlation matrix, which is not
# guaranteed PSD).
ld_matrix <- cor(X)
r_vec <- as.numeric(cor(X, y))
z_scores <- r_vec * sqrt((n_samples - 2) / (1 - r_vec^2))
snp_ids <- sprintf('rs%07d', 1:n_snps)

cat('=== Mandatory LD diagnostic block (estimate_s_rss / kriging_rss) ===\n')
s_hat <- estimate_s_rss(z = z_scores, R = ld_matrix, n = n_samples)
cat(sprintf('estimate_s_rss lambda = %.4f (threshold: <0.05 acceptable, >0.10 refit)\n', s_hat))
cond_z <- kriging_rss(z = z_scores, R = ld_matrix, n = n_samples)
flag_idx <- which(abs(cond_z$conditional_dist$z_std_diff) > 3)
cat(sprintf('kriging_rss flagged %d / %d SNPs with |z_obs - z_exp| > 3\n', length(flag_idx), n_snps))

fit <- susie_rss(z = z_scores, R = ld_matrix, n = n_samples, L = 10, estimate_residual_variance = TRUE)
cat(sprintf('Converged: %s\n', isTRUE(fit$converged)))
cat(sprintf('Effective L used (credible sets returned): %d / requested %d\n', length(fit$sets$cs), 10))

found <- rep(FALSE, length(planted_causal))
for (i in seq_along(fit$sets$cs)) {
  snp_idx <- fit$sets$cs[[i]]
  purity_min <- fit$sets$purity[i, 'min.abs.corr']
  top_snp <- snp_idx[which.max(fit$pip[snp_idx])]
  top_pip <- fit$pip[top_snp]
  hit <- planted_causal[planted_causal %in% snp_idx]
  tag <- if (length(hit) > 0) sprintf('  ** contains planted causal #%s **', paste(which(planted_causal %in% snp_idx), collapse=',')) else ''
  cat(sprintf('Credible set %d: size=%d, purity=%.3f, top=%s (PIP=%.3f)%s\n',
              i, length(snp_idx), purity_min, snp_ids[top_snp], top_pip, tag))
  for (k in seq_along(planted_causal)) if (planted_causal[k] %in% snp_idx) found[k] <- TRUE
}
cat(sprintf('Planted causals recovered: %d / %d\n', sum(found), length(planted_causal)))

purities <- fit$sets$purity[, 'min.abs.corr']
cat('\nASSERT estimate_s_rss lambda < 0.05 for a genuinely matched LD reference:', s_hat < 0.05, '\n')
cat('ASSERT both planted causal variants recovered in a returned credible set:', all(found), '\n')
cat('ASSERT at least one credible set has purity >= 0.5:', any(purities >= 0.5), '\n')
