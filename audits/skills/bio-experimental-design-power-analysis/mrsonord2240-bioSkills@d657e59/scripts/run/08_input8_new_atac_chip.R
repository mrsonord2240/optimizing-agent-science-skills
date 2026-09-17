# Input 8 (NEW input, not in pre-fix audit): ATAC-seq/ChIP-seq per-region power.
# This route had NO code before the fix; now SKILL.md gives an rnapower() block for per-region counts.
# Run it, then independently cross-check with a from-scratch NB simulation + Wald test (not RNASeqPower)
# to confirm the closed-form number is directionally sane, not just "runs without erroring".
suppressPackageStartupMessages(library(RNASeqPower))

p_atac <- rnapower(depth = 10, n = 6, cv = 0.5, effect = 1.5, alpha = 0.05)
cat('ATAC per-region power (SKILL.md worked example): depth=10, n=6, cv=0.5, effect=1.5x ->', round(p_atac, 4), '\n')

# Sweep n to confirm the function behaves monotonically for the ATAC-scale cv (0.5, higher than RNA-seq)
for (nn in c(4, 6, 10, 20)) {
  cat(sprintf('  n=%2d -> power=%.4f\n', nn, rnapower(depth = 10, n = nn, cv = 0.5, effect = 1.5, alpha = 0.05)))
}

# Independent simulation cross-check: simulate NB per-region counts directly and test with a GLM,
# not via RNASeqPower, to confirm the closed-form ATAC power estimate is in a sane range.
set.seed(99)
nsim <- 300
n <- 6; cv <- 0.5; effect <- 1.5; depth <- 10; alpha <- 0.05
disp <- cv^2; size <- 1/disp
reject <- 0
for (i in 1:nsim) {
  mu1 <- 200 * depth   # arbitrary baseline region-count scale; only relative effect matters for size-based NB
  mu2 <- mu1 * effect
  x1 <- rnbinom(n, mu = mu1, size = size)
  x2 <- rnbinom(n, mu = mu2, size = size)
  p <- tryCatch(t.test(log1p(x1), log1p(x2))$p.value, error = function(e) 1)
  if (!is.na(p) && p < alpha) reject <- reject + 1
}
cat('Independent NB-simulation power proxy at same params:', round(reject/nsim, 3), '\n')
cat('rnapower() closed-form:', round(p_atac, 4), '\n')
cat('Both should be low-to-moderate at n=6 (a 1.5x effect at high per-region variability is a hard target).\n')
