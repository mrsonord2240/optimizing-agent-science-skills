# Dataset engineered to land I^2_GX in the 0.6-0.9 SIMEX-rescue band (SKILL.md
# Quantitative Thresholds table). Larger se.exposure relative to spread of
# beta.exposure lowers I^2_GX below the 0.9 NOME-holds cutoff.
set.seed(999)
n <- 20
beta_exposure <- rnorm(n, 0.05, 0.018)
se_exposure   <- rep(0.010, n)   # calibrated (see isq_scan.R) to land I^2_GX ~0.70 -- the 0.6-0.9 SIMEX band
se_outcome    <- rep(0.015, n)
true_causal <- 0.3
beta_outcome <- true_causal * beta_exposure + rnorm(n, 0, 0.010)

dat <- data.frame(
  SNP = paste0('rs', 1:n),
  beta.exposure = beta_exposure, se.exposure = se_exposure,
  beta.outcome = beta_outcome, se.outcome = se_outcome,
  effect_allele.exposure = rep('A', n), other_allele.exposure = rep('G', n),
  effect_allele.outcome = rep('A', n), other_allele.outcome = rep('G', n),
  eaf.exposure = runif(n, 0.15, 0.85), eaf.outcome = runif(n, 0.15, 0.85),
  id.exposure = rep('exposure', n), id.outcome = rep('outcome', n),
  exposure = rep('SimexExposure', n), outcome = rep('SimexOutcome', n),
  mr_keep = rep(TRUE, n), stringsAsFactors = FALSE)
saveRDS(dat, 'F:/OpenScience/audits/bio-causal-genomics-pleiotropy-detection/data/synth_simex.rds')
write.csv(dat, 'F:/OpenScience/audits/bio-causal-genomics-pleiotropy-detection/data/synth_simex.csv', row.names = FALSE)
cat('SIMEX-band dataset written.\n')
