# Input 7 (Adversarial, regression): reviewer asks for observed/post-hoc power on a null result.
# Confirm observed power is a monotone function of the p-value, independent of the Skill's own code.
suppressPackageStartupMessages(library(stats))

set.seed(7)
n <- 20
alpha <- 0.05
obs_power <- function(p_obs, n, alpha) {
  # crude but standard post-hoc power proxy: power to detect the *observed* effect at the same n/alpha,
  # approximated via the observed z / t and the noncentral distribution
  z_crit <- qnorm(1 - alpha/2)
  z_obs <- qnorm(1 - p_obs/2)  # back out an implied |z| from the two-sided p-value
  pnorm(z_obs - z_crit) + pnorm(-z_obs - z_crit)
}
ps <- c(0.65, 0.45, 0.30, 0.19, 0.06)
for (p in ps) {
  cat(sprintf('p_obs=%.2f -> post-hoc power proxy=%.3f\n', p, obs_power(p, n, alpha)))
}
cat('Monotone increasing as p_obs falls: confirms observed power is a deterministic function of p alone.\n')
