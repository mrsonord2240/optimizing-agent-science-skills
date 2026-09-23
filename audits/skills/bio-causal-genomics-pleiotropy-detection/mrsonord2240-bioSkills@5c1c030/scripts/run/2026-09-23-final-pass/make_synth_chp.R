# Synthetic instrument-level MR dataset with a PLANTED correlated horizontal
# pleiotropy (CHP) mechanism -- ground truth: TRUE CAUSAL EFFECT = 0. All of the
# exposure-outcome association observed by UHP-blind methods (IVW/Egger/PRESSO)
# is manufactured by a shared upstream confounder U whose per-SNP loading on the
# outcome is correlated with each SNP's exposure effect (violates InSIDE).
# This directly instantiates SKILL.md's "MR-PRESSO false negative under CHP"
# failure mode (see Per-Method Failure Modes section) so we can check empirically
# whether PRESSO's global test in fact stays non-significant while IVW is biased.
set.seed(20260917)
n <- 40
beta_exposure <- abs(rnorm(n, 0.05, 0.015))       # gamma_j: instrument-exposure effect
se_exposure   <- rep(0.008, n)
se_outcome    <- rep(0.010, n)

true_causal <- 0                                   # <-- ground truth: NO real causal effect
k_chp <- 0.9                                        # CHP loading: alpha_j = k * gamma_j + noise
alpha_chp <- k_chp * beta_exposure + rnorm(n, 0, 0.004)   # correlated with gamma -> CHP, not UHP

beta_outcome <- true_causal * beta_exposure + alpha_chp + rnorm(n, 0, 0.004)

dat <- data.frame(
  SNP = paste0('rs', 1:n),
  beta.exposure = beta_exposure, se.exposure = se_exposure,
  beta.outcome = beta_outcome, se.outcome = se_outcome,
  effect_allele.exposure = rep('A', n), other_allele.exposure = rep('G', n),
  effect_allele.outcome = rep('A', n), other_allele.outcome = rep('G', n),
  eaf.exposure = runif(n, 0.15, 0.85), eaf.outcome = runif(n, 0.15, 0.85),
  id.exposure = rep('exposure', n), id.outcome = rep('outcome', n),
  exposure = rep('SyntheticExposure', n), outcome = rep('SyntheticOutcome', n),
  mr_keep = rep(TRUE, n), stringsAsFactors = FALSE)

saveRDS(dat, 'F:/OpenScience/audits/bio-causal-genomics-pleiotropy-detection/data/synth_chp.rds')
write.csv(dat, 'F:/OpenScience/audits/bio-causal-genomics-pleiotropy-detection/data/synth_chp.csv', row.names = FALSE)
cat('Synthetic CHP dataset written. n =', n, ' true_causal =', true_causal, ' k_chp =', k_chp, '\n')
cat('Correlation(alpha_chp, beta_exposure):', round(cor(alpha_chp, beta_exposure), 3), '(should be high -- CHP, not UHP)\n')
