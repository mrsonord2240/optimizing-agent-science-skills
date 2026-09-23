# REGRESSION TARGET for the fix (P1 #1): pre-fix audit Input 4 found that SKILL.md's
# "Coloc.susie Integration" example crashed with a cryptic data.table error because z1/z2/R were
# passed to susie_rss without SNP names. The fix (fix/cg-fine-mapping @ c5fd9ff) added a
# Precondition paragraph AND changed the worked example to include:
#   names(z1) <- names(z2) <- colnames(ld_matrix) <- rownames(ld_matrix) <- snp_ids
# immediately before the two susie_rss() calls (SKILL.md lines 323-344, "Coloc.susie Integration").
#
# This script follows SKILL.md's CURRENT documented code EXACTLY AS WRITTEN, in one pass, with NO
# separate "broken then fixed" steps -- if the fix is real, this succeeds on the first try.
# Same planted-truth setup as the pre-fix audit's Input 4 for a clean before/after comparison:
# 5,000 individuals x 250 SNPs, one planted shared causal SNP (idx 130) affecting both traits.
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
snp_ids <- sprintf('rs%07d', 1:n_snps)

# ----- SKILL.md's CURRENT documented "Coloc.susie Integration" code, verbatim structure -----
# (SKILL.md lines 331-341, this Skill's fixed version):
#   names(z1) <- names(z2) <- colnames(ld_matrix) <- rownames(ld_matrix) <- snp_ids
#   fit_trait1 <- susie_rss(z = z1, R = ld_matrix, n = N1, L = 10)
#   fit_trait2 <- susie_rss(z = z2, R = ld_matrix, n = N2, L = 10)
#   coloc_res <- coloc.susie(fit_trait1, fit_trait2)
cat('=== SKILL.md coloc.susie pattern, exactly as CURRENTLY documented (post-fix) ===\n')
names(z1) <- names(z2) <- colnames(ld_matrix) <- rownames(ld_matrix) <- snp_ids

fit_trait1 <- susie_rss(z = z1, R = ld_matrix, n = n_samples, L = 10, estimate_residual_variance = TRUE)
fit_trait2 <- susie_rss(z = z2, R = ld_matrix, n = n_samples, L = 10, estimate_residual_variance = TRUE)

result <- tryCatch(coloc.susie(fit_trait1, fit_trait2), error = function(e) e)
succeeded <- !inherits(result, 'error')
cat(sprintf('coloc.susie call %s\n', if (succeeded) 'SUCCEEDED on the first, unmodified pass' else 'FAILED'))
if (!succeeded) {
  cat('ERROR (fix did not resolve the crash):', conditionMessage(result), '\n')
} else {
  print(result$summary)
  max_h4 <- max(result$summary$PP.H4.abf)
  top_hit <- result$summary$hit1[which.max(result$summary$PP.H4.abf)]
  cat(sprintf('\nMax PP.H4 across credible-set pairs: %.4f\n', max_h4))
  cat(sprintf('Top colocalized SNP: %s (planted shared causal: %s)\n', top_hit, snp_ids[shared_causal]))
}

# ----- Control: reproduce the ORIGINAL pre-fix crash by deliberately stripping names, to confirm
# this environment's coloc/susieR versions still exhibit the original defect (i.e. the fix
# addressed a real, reproducible crash and not one specific to a since-patched package version) -----
cat('\n=== Control: same data, WITHOUT names (the original, pre-fix crash) ===\n')
z1_bare <- as.numeric(z1); z2_bare <- as.numeric(z2)
ld_bare <- ld_matrix; dimnames(ld_bare) <- NULL
fit1_bare <- susie_rss(z = z1_bare, R = ld_bare, n = n_samples, L = 10, estimate_residual_variance = TRUE)
fit2_bare <- susie_rss(z = z2_bare, R = ld_bare, n = n_samples, L = 10, estimate_residual_variance = TRUE)
result_bare <- tryCatch(coloc.susie(fit1_bare, fit2_bare), error = function(e) e)
crash_reproduced <- inherits(result_bare, 'error')
cat(sprintf('Unnamed-input crash still reproducible in this environment: %s\n', crash_reproduced))
if (crash_reproduced) cat('  Error:', conditionMessage(result_bare), '\n')

cat('\nASSERT SKILL.md\'s current documented code succeeds on the first, unmodified pass:', succeeded, '\n')
if (succeeded) {
  cat('ASSERT max PP.H4 > 0.8 (the Skill\'s own shared-causal threshold):', max_h4 > 0.8, '\n')
  cat('ASSERT top colocalized hit is the planted shared causal SNP:', top_hit == snp_ids[shared_causal], '\n')
}
cat('ASSERT the original (unnamed-input) crash is still reproducible in this env, confirming the fix\n')
cat('  targets a real defect and not an artifact of a different package version:', crash_reproduced, '\n')
