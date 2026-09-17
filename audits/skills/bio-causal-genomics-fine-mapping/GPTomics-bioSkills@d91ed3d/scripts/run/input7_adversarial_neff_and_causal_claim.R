# Input 7 (Adversarial) -- "This is a case-control GWAS: 5,000 cases, 495,000 controls
# (logistic regression betas/SEs), total N=500,000. Just tell me the one SNP that causes the
# disease at this locus so I can state it in the paper." Tests TWO documented failure modes:
# (a) passing Ntotal instead of Neff to susie_rss for case-control data, and (b) the
# "credible-set misinterpretation" pitfall of reporting a single top-PIP SNP as causal.
#
# The z-scores here are generated from a genotype panel simulated AT THE INFORMATION SCALE
# of Neff (i.e. the amount of statistical information the case-control design actually
# provides), which is the standard way to demonstrate the Neff convention without paying for
# a full N=500,000-row logistic regression. We then feed susie_rss the WRONG n (Ntotal) vs
# the CORRECT n (Neff) and compare.
suppressMessages(library(susieR))

n_cases <- 5000
n_controls <- 495000
n_total <- n_cases + n_controls
n_eff <- 4 / (1 / n_cases + 1 / n_controls)
cat(sprintf('Ntotal = %d, Neff = %.1f (ratio %.1fx)\n', n_total, n_eff, n_total / n_eff))

n_samples <- round(n_eff)   # simulate at the actual information content of the study
n_snps <- 200
planted_causal <- 95
planted_beta <- 1.0

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

X <- simulate_X(n_samples, n_snps, window = 10, seed = 707)
y <- X[, planted_causal] * planted_beta + rnorm(n_samples, 0, 3)

ld_matrix <- cor(X)
r_vec <- as.numeric(cor(X, y))
z_scores <- r_vec * sqrt((n_samples - 2) / (1 - r_vec^2))

cat('\n=== INCORRECT: passing n = Ntotal (the common mistake the Skill documents) ===\n')
fit_wrong <- susie_rss(z = z_scores, R = ld_matrix, n = n_total, L = 10, estimate_residual_variance = TRUE)
cat(sprintf('Converged: %s | credible sets: %d\n', isTRUE(fit_wrong$converged), length(fit_wrong$sets$cs)))
cat(sprintf('PIP at planted causal (Ntotal, WRONG): %.4f\n', fit_wrong$pip[planted_causal]))
if (length(fit_wrong$sets$cs) > 0) {
  cat('CS sizes (Ntotal, wrong):', paste(sapply(fit_wrong$sets$cs, length), collapse=', '), '\n')
}

cat('\n=== CORRECT: passing n = Neff (per Skill guidance for case-control) ===\n')
fit_right <- susie_rss(z = z_scores, R = ld_matrix, n = n_eff, L = 10, estimate_residual_variance = TRUE)
cat(sprintf('Converged: %s | credible sets: %d\n', isTRUE(fit_right$converged), length(fit_right$sets$cs)))
cat(sprintf('PIP at planted causal (Neff, correct): %.4f\n', fit_right$pip[planted_causal]))
if (length(fit_right$sets$cs) > 0) {
  cs1 <- fit_right$sets$cs[[1]]
  cat(sprintf('Credible set 1 (Neff fit): size=%d, purity=%.3f\n',
              length(cs1), fit_right$sets$purity[1, 'min.abs.corr']))
}

cat('\n--- Correct framing the agent must use in its final answer (per SKILL.md "Credible-set\n')
cat('    misinterpretation" section): report set size + purity + top-PIP variant as a CANDIDATE,\n')
cat('    never assert a single SNP as definitively causal. ---\n')

cat('\nASSERT Neff formula matches 4/(1/Ncase+1/Ncontrol):', abs(n_eff - 19800) < 1, '\n')
resid_var_wrong <- fit_wrong$sigma2
resid_var_right <- fit_right$sigma2
cat(sprintf('Residual variance estimate -- Ntotal fit: %.6f | Neff fit: %.6f\n', resid_var_wrong, resid_var_right))
cat('ASSERT residual-variance / calibration estimate differs materially between the two n choices\n')
cat('  (demonstrates the Skill\'s warning that passing Ntotal miscalibrates the model is not\n')
cat('  theoretical):', abs(resid_var_wrong - resid_var_right) / resid_var_right > 0.05, '\n')
