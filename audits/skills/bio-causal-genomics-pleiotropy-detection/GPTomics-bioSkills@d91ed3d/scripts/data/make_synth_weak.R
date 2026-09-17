# Weak-instrument synthetic dataset (mean F < 10). Ground truth causal effect = 0.25.
set.seed(555)
n <- 25
beta_exposure <- rnorm(n, 0.015, 0.008)   # small, noisy exposure effects -> low F
se_exposure   <- rep(0.010, n)
se_outcome    <- rep(0.012, n)
true_causal <- 0.25
beta_outcome <- true_causal * beta_exposure + rnorm(n, 0, 0.010)

dat <- data.frame(
  SNP = paste0('rs', 1:n),
  beta.exposure = beta_exposure, se.exposure = se_exposure,
  beta.outcome = beta_outcome, se.outcome = se_outcome,
  effect_allele.exposure = rep('A', n), other_allele.exposure = rep('G', n),
  effect_allele.outcome = rep('A', n), other_allele.outcome = rep('G', n),
  eaf.exposure = runif(n, 0.15, 0.85), eaf.outcome = runif(n, 0.15, 0.85),
  id.exposure = rep('exposure', n), id.outcome = rep('outcome', n),
  exposure = rep('WeakExposure', n), outcome = rep('WeakOutcome', n),
  mr_keep = rep(TRUE, n), stringsAsFactors = FALSE)
f <- (beta_exposure / se_exposure)^2
saveRDS(dat, 'F:/OpenScience/audits/bio-causal-genomics-pleiotropy-detection/data/synth_weak.rds')
write.csv(dat, 'F:/OpenScience/audits/bio-causal-genomics-pleiotropy-detection/data/synth_weak.csv', row.names = FALSE)
cat('Weak-instrument dataset written. Mean F =', round(mean(f),2), ' true_causal =', true_causal, '\n')
