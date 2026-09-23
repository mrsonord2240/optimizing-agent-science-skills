# 18-SNP instrument set with TWO distinct causal mechanisms (heterogeneous Wald
# ratios): cluster A ~0.2, cluster B ~0.6, ground truth for MR-Clust recovery.
# Deliberately n<20 to test whether the agent flags the Skill's own documented
# MR-Mix minimum ("Need >=20 SNPs" -- SKILL.md Common Errors table) while still
# being usable for MR-Clust (no stated minimum in the Skill beyond 'enough to
# cluster').
set.seed(321)
n_a <- 9; n_b <- 9
n <- n_a + n_b
beta_exposure <- abs(rnorm(n, 0.05, 0.012))
se_exposure <- rep(0.009, n)
se_outcome  <- rep(0.011, n)
true_a <- 0.2; true_b <- 0.6
beta_outcome <- c(true_a * beta_exposure[1:n_a] + rnorm(n_a, 0, 0.004),
                  true_b * beta_exposure[(n_a+1):n] + rnorm(n_b, 0, 0.004))

dat <- data.frame(
  SNP = paste0('rs', 1:n),
  beta.exposure = beta_exposure, se.exposure = se_exposure,
  beta.outcome = beta_outcome, se.outcome = se_outcome,
  effect_allele.exposure = rep('A', n), other_allele.exposure = rep('G', n),
  effect_allele.outcome = rep('A', n), other_allele.outcome = rep('G', n),
  eaf.exposure = runif(n, 0.15, 0.85), eaf.outcome = runif(n, 0.15, 0.85),
  id.exposure = rep('exposure', n), id.outcome = rep('outcome', n),
  exposure = rep('ClusterExposure', n), outcome = rep('ClusterOutcome', n),
  mr_keep = rep(TRUE, n), stringsAsFactors = FALSE)
saveRDS(dat, 'F:/OpenScience/audits/bio-causal-genomics-pleiotropy-detection/data/synth_clusters.rds')
write.csv(dat, 'F:/OpenScience/audits/bio-causal-genomics-pleiotropy-detection/data/synth_clusters.csv', row.names = FALSE)
cat('Cluster dataset written. n =', n, ' true_a =', true_a, ' true_b =', true_b, '\n')
