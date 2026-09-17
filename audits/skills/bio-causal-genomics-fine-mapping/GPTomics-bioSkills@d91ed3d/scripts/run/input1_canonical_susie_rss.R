# Input 1 (Canonical) -- "Fine-map a 1 Mb window around a lead SNP using susie_rss with a
# matched LD reference. Run estimate_s_rss and report lambda. Extract 95% credible sets,
# purity, and top PIP variants." Follows the Skill's Critical LD Diagnostic Block, then its
# purity-filtered credible-set extraction pattern (examples/susie_rss_finemap.R).
#
# Synthetic locus, 2 planted causal variants. Genotypes are simulated first (latent-factor
# LD blocks, as in a real cohort), then z-scores and R are BOTH derived from that same
# genotype matrix -- guaranteeing genuine internal consistency (a truly matched LD
# reference), unlike hand-written banded correlation matrices which are not guaranteed PSD.
suppressMessages(library(susieR))

set.seed(101)
n_samples <- 6000
n_snps <- 400
planted_causal <- c(90, 310)
planted_beta   <- c(0.9, -0.75)

simulate_X <- function(n_samples, n_snps, window = 15, seed) {
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

X <- simulate_X(n_samples, n_snps, seed = 101)
y <- X[, planted_causal[1]] * planted_beta[1] + X[, planted_causal[2]] * planted_beta[2] + rnorm(n_samples, 0, 3)

# Per-SNP GWAS summary stats derived from this exact cohort (guarantees z consistent with R)
r_vec <- as.numeric(cor(X, y))
z_scores <- r_vec * sqrt((n_samples - 2) / (1 - r_vec^2))
ld_matrix <- cor(X)
snp_ids <- sprintf('rs%07d', 1:n_snps)

cat('=== Mandatory LD diagnostic block ===\n')
s_hat <- estimate_s_rss(z = z_scores, R = ld_matrix, n = n_samples)
cat(sprintf('estimate_s_rss lambda = %.4f (threshold: <0.05 acceptable, >0.10 refit)\n', s_hat))

cond_z <- kriging_rss(z = z_scores, R = ld_matrix, n = n_samples)
flag_idx <- which(abs(cond_z$conditional_dist$z_std_diff) > 3)
cat(sprintf('kriging_rss flagged %d / %d SNPs with |z_obs - z_exp| > 3\n', length(flag_idx), n_snps))

cat('\n=== susie_rss fit (L=10) ===\n')
fit <- susie_rss(z = z_scores, R = ld_matrix, n = n_samples, L = 10, estimate_residual_variance = TRUE)
cat(sprintf('Converged: %s\n', isTRUE(fit$converged)))
cat(sprintf('Effective L used (credible sets returned): %d / requested 10\n', length(fit$sets$cs)))

cs_list <- fit$sets$cs
purity_mat <- fit$sets$purity
found_causal <- rep(FALSE, length(planted_causal))

for (i in seq_along(cs_list)) {
  snp_idx <- cs_list[[i]]
  purity_min <- purity_mat[i, 'min.abs.corr']
  top_snp <- snp_idx[which.max(fit$pip[snp_idx])]
  cat(sprintf('Credible set %d: size=%d, purity=%.3f, top=%s (PIP=%.3f)\n',
              i, length(snp_idx), purity_min, snp_ids[top_snp], fit$pip[top_snp]))
  for (k in seq_along(planted_causal)) {
    if (planted_causal[k] %in% snp_idx) {
      found_causal[k] <- TRUE
      cat(sprintf('  ** contains planted causal #%d (idx %d, true beta=%.3f) **\n',
                  k, planted_causal[k], planted_beta[k]))
    }
  }
}

cat(sprintf('\nPlanted causals recovered: %d / %d\n', sum(found_causal), length(planted_causal)))
cat(sprintf('PIP at planted causal 1 (idx %d): %.4f\n', planted_causal[1], fit$pip[planted_causal[1]]))
cat(sprintf('PIP at planted causal 2 (idx %d): %.4f\n', planted_causal[2], fit$pip[planted_causal[2]]))
cat('ASSERT s_hat < 0.05 (genuinely matched LD):', s_hat < 0.05, '\n')
cat('ASSERT both planted causals recovered in some CS:', all(found_causal), '\n')
cat('ASSERT at least one CS has purity >= 0.5:', any(purity_mat[, 'min.abs.corr'] >= 0.5), '\n')
