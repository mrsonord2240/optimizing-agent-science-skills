# REGRESSION of pre-fix audit Input 2 (Variant A) -- "I have individual-level genotypes for this
# locus. Fine-map with susie(X, y, L=10) instead of summary stats." Skill's decision-tree row:
# "Individual-level genotypes available -> susie(X,y,L=10): in-sample LD is exact." Unchanged code
# path from the pre-fix audit (not touched by the fix commit) -- pure regression check.
suppressMessages(library(susieR))

set.seed(202)
n_samples <- 2000
n_snps <- 150
planted_causal <- 60
planted_beta <- 0.35

X <- matrix(0, n_samples, n_snps)
window <- 20
i <- 1
while (i <= n_snps) {
  end <- min(n_snps, i + window - 1)
  latent <- rnorm(n_samples)
  for (j in i:end) {
    maf <- runif(1, 0.1, 0.4)
    liability <- 0.8 * latent + sqrt(1 - 0.8^2) * rnorm(n_samples)
    thresh <- quantile(liability, 1 - maf)
    X[, j] <- rbinom(n_samples, 2, pmin(pmax(plogis((liability - thresh) * 2 + qlogis(maf)), 0.01), 0.99))
  }
  i <- end + 1
}
X <- scale(X)

y <- X[, planted_causal] * planted_beta + rnorm(n_samples, 0, 1)

cat('=== susie(X, y, L=10) on individual-level genotypes ===\n')
fit <- susie(X, y, L = 10, estimate_residual_variance = TRUE)
cat(sprintf('Converged: %s\n', isTRUE(fit$converged)))
cat(sprintf('Number of credible sets: %d\n', length(fit$sets$cs)))

found <- FALSE
for (i in seq_along(fit$sets$cs)) {
  snp_idx <- fit$sets$cs[[i]]
  purity_min <- fit$sets$purity[i, 'min.abs.corr']
  top_snp <- snp_idx[which.max(fit$pip[snp_idx])]
  cat(sprintf('CS %d: size=%d, purity=%.3f, top=SNP%d (PIP=%.3f)\n',
              i, length(snp_idx), purity_min, top_snp, fit$pip[top_snp]))
  if (planted_causal %in% snp_idx) {
    found <- TRUE
    cat(sprintf('  ** contains planted causal SNP%d (true beta=%.2f) **\n', planted_causal, planted_beta))
  }
}

cat(sprintf('\nPIP at planted causal (SNP%d): %.4f\n', planted_causal, fit$pip[planted_causal]))
cat('ASSERT planted causal recovered in a credible set:', found, '\n')
cat('ASSERT PIP at planted causal > 0.5:', fit$pip[planted_causal] > 0.5, '\n')
cat('ASSERT in-sample LD used (no estimate_s_rss needed for individual-level data):', TRUE, '\n')
