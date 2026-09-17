# Input 4 (Variant B) -- "Fine-map trait1 and trait2 separately at the same locus (they share
# an LD reference from the same source population), then run coloc.susie. Report PP.H4 per
# credible-set pair." Follows the Skill's "Coloc.susie Integration" section VERBATIM
# (SKILL.md lines 320-337: `fit1 <- susie_rss(z=z1,...); fit2 <- susie_rss(z=z2,...);
# coloc_res <- coloc.susie(fit1, fit2)` -- no SNP names anywhere in that documented pattern).
#
# Planted ground truth: both traits share ONE causal variant at this locus; z-scores for
# each trait are derived from the SAME genotype matrix (a realistic shared-LD-reference
# colocalization setup).
suppressMessages({ library(susieR); library(coloc) })

set.seed(404)
n_samples <- 5000
n_snps <- 250
shared_causal <- 130

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

X <- simulate_X(n_samples, n_snps, window = 12, seed = 404)
y1 <- X[, shared_causal] * 1.0 + rnorm(n_samples, 0, 3)
y2 <- X[, shared_causal] * 0.7 + rnorm(n_samples, 0, 3)

ld_matrix <- cor(X)
r1 <- as.numeric(cor(X, y1)); z1 <- r1 * sqrt((n_samples - 2) / (1 - r1^2))
r2 <- as.numeric(cor(X, y2)); z2 <- r2 * sqrt((n_samples - 2) / (1 - r2^2))

# ----- Step A: run the SKILL.md pattern EXACTLY as documented (bare, unnamed z vectors) -----
cat('=== Step A: SKILL.md coloc.susie pattern, exactly as documented (no SNP names) ===\n')
fit1 <- susie_rss(z = z1, R = ld_matrix, n = n_samples, L = 10, estimate_residual_variance = TRUE)
fit2 <- susie_rss(z = z2, R = ld_matrix, n = n_samples, L = 10, estimate_residual_variance = TRUE)
cat(sprintf('Trait1 credible sets: %d, Trait2 credible sets: %d\n',
            length(fit1$sets$cs), length(fit2$sets$cs)))

res_undocumented <- tryCatch(coloc.susie(fit1, fit2), error = function(e) e)
if (inherits(res_undocumented, 'error')) {
  cat('coloc.susie ERROR (following SKILL.md exactly):', conditionMessage(res_undocumented), '\n')
  cat('DIAGNOSIS: fit1$lbf_variable / fit2$lbf_variable have NULL colnames because z1/z2 were\n')
  cat('  unnamed vectors, so coloc.bf_bf finds isnps = intersect(colnames(bf1), colnames(bf2))\n')
  cat('  = character(0) and silently returns data.table(nsnps=NA) with no $summary field --\n')
  cat('  coloc.susie then crashes on ret$summary[, :=(...)] with a cryptic data.table error that\n')
  cat('  never mentions the real cause (missing SNP names). SKILL.md never states this precondition.\n')
} else {
  cat('Unexpectedly succeeded without names -- printing result:\n'); print(res_undocumented$summary)
}

# ----- Step B: identical run, with SNP names added (undocumented but required precondition) -----
cat('\n=== Step B: same data, with SNP/LD names added (the actual fix) ===\n')
snp_ids <- sprintf('rs%07d', 1:n_snps)
names(z1) <- snp_ids; names(z2) <- snp_ids
colnames(ld_matrix) <- rownames(ld_matrix) <- snp_ids

fit1n <- susie_rss(z = z1, R = ld_matrix, n = n_samples, L = 10, estimate_residual_variance = TRUE)
fit2n <- susie_rss(z = z2, R = ld_matrix, n = n_samples, L = 10, estimate_residual_variance = TRUE)
coloc_res <- coloc.susie(fit1n, fit2n)
cat('coloc.susie SUCCEEDED with named z/R:\n')
print(coloc_res$summary)
max_h4 <- max(coloc_res$summary$PP.H4.abf)
cat(sprintf('\nMax PP.H4 across credible-set pairs: %.4f\n', max_h4))
top_hit <- coloc_res$summary$hit1[which.max(coloc_res$summary$PP.H4.abf)]
cat(sprintf('Top colocalized SNP: %s (planted shared causal: %s)\n', top_hit, snp_ids[shared_causal]))

cat('\nASSERT coloc.susie FAILS when SKILL.md\'s documented pattern is followed literally (unnamed z):',
    inherits(res_undocumented, 'error'), '\n')
cat('ASSERT coloc.susie SUCCEEDS once SNP names are added (confirms underlying method works):',
    !is.null(coloc_res$summary), '\n')
cat('ASSERT max PP.H4 > 0.8 (shared-causal threshold per Skill):', max_h4 > 0.8, '\n')
cat('ASSERT top colocalized hit is the planted shared causal SNP:', top_hit == snp_ids[shared_causal], '\n')
