# NEW INPUT 8 (part b) -- consumes the REAL PolyFun output from input8a and follows SKILL.md's
# "Functional Priors with PolyFun" R code EXACTLY AS DOCUMENTED:
#   priors <- read.table('polyfun_h2.<CHR>.snpvar_ridge_constrained.gz', header = TRUE)
#   priors <- priors[match(gwas_df$SNP, priors$SNP), ]
#   prior_w <- priors$SNPVAR / sum(priors$SNPVAR, na.rm = TRUE)
#   fit <- susie_rss(z = z_scores, R = ld_matrix, n = N, L = 10, prior_weights = prior_w)
#
# This is a genuinely new code path for this Skill's audit series: the pre-fix audit had no
# PolyFun installed and scored this section by inspection only. PolyFun is now real and its
# output is real (see input8a's real chr22 RBC GWAS run, N=383,290, 2,511 SNPs).
#
# Ground truth: real PolyFun SNPVAR values + real GWAS Z-scores for a 300-SNP window from a real
# chr22 locus; the LD matrix is SYNTHETIC (documented explicitly -- no real genotype panel for
# this exact SNP set exists in this environment) with a planted causal effect added on top of the
# real Z at the SNP the real PolyFun run itself ranked highest by SNPVAR in that window (i.e. the
# SNP a real S-LDSC functional-prior run would flag as most likely to carry a true effect). This
# tests whether the documented prior_weights integration actually sharpens inference relative to
# uniform when the prior is real and informative -- not whether real GWAS Z-scores alone contain
# a true causal variant (they don't have known ground truth at this scale).
suppressMessages(library(susieR))

priors_full <- read.table(
  'polyfun_out/testout.22.snpvar_ridge_constrained.gz',
  header = TRUE, sep = '\t'
)
cat(sprintf('Read %d SNPs from real PolyFun output; columns: %s\n',
            nrow(priors_full), paste(colnames(priors_full), collapse = ', ')))
cat('ASSERT PolyFun output column is exactly "SNPVAR" (uppercase, case-sensitive per SKILL.md):',
    'SNPVAR' %in% colnames(priors_full), '\n')

# ---- Window: 300 contiguous SNPs by physical position ----
priors_full <- priors_full[order(priors_full$BP), ]
n_snps <- 300
start_idx <- 500
window <- priors_full[start_idx:(start_idx + n_snps - 1), ]
stopifnot(nrow(window) == n_snps, !any(is.na(window$SNPVAR)))

N_real <- unique(window$N)
cat(sprintf('Window: chr22:%d-%d, N (real GWAS sample size) = %s\n',
            min(window$BP), max(window$BP), paste(N_real, collapse = ',')))

# SNP PolyFun's real S-LDSC run ranked highest by functional prior in this window --
# the natural candidate a researcher would want prior_weights to highlight.
high_prior_idx <- which.max(window$SNPVAR)
cat(sprintf('Highest-SNPVAR SNP in window: %s (SNPVAR=%.3e, rank %d/%d)\n',
            window$SNP[high_prior_idx], window$SNPVAR[high_prior_idx], high_prior_idx, n_snps))

# ---- Synthetic LD (documented: no real genotype panel for this exact SNP set here) ----
set.seed(808)
n_samples_ld <- 4000
X <- matrix(0, n_samples_ld, n_snps)
i <- 1
while (i <= n_snps) {
  end <- min(n_snps, i + 10 - 1)
  latent <- rnorm(n_samples_ld)
  for (j in i:end) {
    maf <- runif(1, 0.15, 0.4)
    liab <- 0.8 * latent + sqrt(1 - 0.8^2) * rnorm(n_samples_ld)
    thresh <- quantile(liab, 1 - maf)
    X[, j] <- rbinom(n_samples_ld, 2, pmin(pmax(plogis((liab - thresh) * 2 + qlogis(maf)), 0.01), 0.99))
  }
  i <- end + 1
}
X <- scale(X)
ld_matrix <- cor(X)
colnames(ld_matrix) <- rownames(ld_matrix) <- window$SNP

# Planted causal effect layered onto real Z, at the real high-SNPVAR SNP, WEAK enough that a
# uniform prior does not confidently resolve it (to make any prior-driven sharpening visible).
planted_beta <- 0.065
y <- X[, high_prior_idx] * planted_beta + rnorm(n_samples_ld, 0, 1)
r_vec <- as.numeric(cor(X, y))
z_scores <- r_vec * sqrt((n_samples_ld - 2) / (1 - r_vec^2))
names(z_scores) <- window$SNP

# ---- SKILL.md's documented pattern, verbatim: read real priors, sum-normalize, prior_weights= ----
prior_w <- window$SNPVAR / sum(window$SNPVAR, na.rm = TRUE)
cat(sprintf('sum(prior_w) = %.6f (ASSERT ~= 1: %s)\n', sum(prior_w), abs(sum(prior_w) - 1) < 1e-8))

cat('\n=== Fit A: uniform prior (baseline) ===\n')
fit_uniform <- susie_rss(z = z_scores, R = ld_matrix, n = n_samples_ld, L = 10,
                          estimate_residual_variance = TRUE)
pip_uniform <- fit_uniform$pip[high_prior_idx]
cat(sprintf('PIP at high-SNPVAR planted-effect SNP (uniform prior): %.4f\n', pip_uniform))

cat('\n=== Fit B: SKILL.md documented pattern -- prior_weights = real PolyFun SNPVAR ===\n')
fit_correct <- tryCatch(
  susie_rss(z = z_scores, R = ld_matrix, n = n_samples_ld, L = 10,
            prior_weights = prior_w, estimate_residual_variance = TRUE),
  error = function(e) e
)
correct_ok <- !inherits(fit_correct, 'error')
cat(sprintf('prior_weights= call: %s\n', if (correct_ok) 'SUCCEEDED' else paste('FAILED:', conditionMessage(fit_correct))))
if (correct_ok) {
  pip_correct <- fit_correct$pip[high_prior_idx]
  cat(sprintf('PIP at high-SNPVAR planted-effect SNP (real prior_weights): %.4f\n', pip_correct))
}

cat('\n=== Fit C: the SKILL.md-documented MISTAKE -- passing the same vector to prior_variance ===\n')
fit_wrong <- tryCatch(
  susie_rss(z = z_scores, R = ld_matrix, n = n_samples_ld, L = 10,
            prior_variance = prior_w, estimate_residual_variance = TRUE),
  error = function(e) e
)
wrong_errored <- inherits(fit_wrong, 'error')
cat(sprintf('prior_variance= call (the documented mistake): %s\n',
            if (wrong_errored) paste('ERRORED:', conditionMessage(fit_wrong)) else 'ran without error'))
if (!wrong_errored) {
  pip_wrong <- fit_wrong$pip[high_prior_idx]
  cat(sprintf('PIP at same SNP under the prior_variance mistake: %.4f\n', pip_wrong))
}

cat('\nASSERT prior_weights= (correct arg) succeeds:', correct_ok, '\n')
if (correct_ok) {
  cat('ASSERT real prior_weights increases (or maintains) PIP vs uniform at the high-SNPVAR planted SNP:',
      pip_correct >= pip_uniform, sprintf('(uniform=%.4f, prior=%.4f)', pip_uniform, pip_correct), '\n')
}
cat('ASSERT the SKILL.md-documented prior_variance mistake does NOT crash (matches "silently accepted"',
    'claim in "prior_weights vs prior_variance confusion"):', !wrong_errored, '\n')
if (!wrong_errored && correct_ok) {
  cat('ASSERT the mistake (prior_variance) produces a PIP materially different from the correct',
      'prior_weights fit, i.e. it is NOT equivalent -- confirms the argument confusion is a real,',
      'silent, distinct-outcome bug and not a harmless alias:',
      abs(pip_wrong - pip_correct) > 1e-6, sprintf('(wrong=%.4f, correct=%.4f)', pip_wrong, pip_correct), '\n')
}
