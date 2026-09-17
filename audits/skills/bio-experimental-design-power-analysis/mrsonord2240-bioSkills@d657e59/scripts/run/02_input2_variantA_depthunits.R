# Input 2 (Variant A, regression + extends the fix): verify the new "Depth Units" conversion
# is internally consistent and independently correct against a from-scratch NB power simulation
# (not the Skill's own rnapower(), an independent check).
suppressPackageStartupMessages(library(RNASeqPower))

reads_millions <- 20
depth_conservative <- 0.1 * reads_millions
cat('SKILL.md worked example check: depth(20M reads) =', depth_conservative, '\n')

p_conservative <- rnapower(depth = depth_conservative, n = 14, cv = 0.3, effect = 1.5, alpha = 0.05)
p_deep <- rnapower(depth = 20, n = 14, cv = 0.3, effect = 1.5, alpha = 0.05)
cat('power at depth=2 (20M reads, conservative), n=14:', round(p_conservative, 3), '\n')
cat('power at depth=20 (SKILL.md flagship example), n=14:', round(p_deep, 3), '\n')
cat('SKILL.md claims ~0.29 vs ~0.82 -- reproduced:', round(p_conservative,2), round(p_deep,2), '\n')

# Independent cross-check: simulate NB counts directly (not via RNASeqPower) and run a Wald test,
# to confirm the closed-form power at depth=20 is in the right ballpark, not just internally consistent.
set.seed(42)
nb_power_sim <- function(depth, n, cv, effect, alpha, nsim = 400, ngene_mean = 500) {
  disp <- cv^2   # NB dispersion parameterization consistent with cv = 1/sqrt(size) at high mean
  size <- 1 / disp
  reject <- 0
  for (i in 1:nsim) {
    mu1 <- ngene_mean * depth
    mu2 <- mu1 * effect
    x1 <- rnbinom(n, mu = mu1, size = size)
    x2 <- rnbinom(n, mu = mu2, size = size)
    # simple two-sample t-test on log-counts as an independent, crude power proxy
    p <- tryCatch(t.test(log1p(x1), log1p(x2))$p.value, error = function(e) 1)
    if (!is.na(p) && p < alpha) reject <- reject + 1
  }
  reject / nsim
}
sim_power_d20 <- nb_power_sim(depth = 20, n = 14, cv = 0.3, effect = 1.5, alpha = 0.05)
cat('Independent NB-simulation power (log-count t-test proxy) at depth=20, n=14:', round(sim_power_d20, 3), '\n')
cat('rnapower() closed-form at the same params:', round(p_deep, 3), '\n')
cat('Both should indicate reasonably high power (>0.5); a crude proxy will not match exactly.\n')
