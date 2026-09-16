.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# Input 3 (Edge), part b -- how stable is the pi0 estimate the SKILL.md tells the
# analyst to report, as the family shrinks?  500 replicate ALL-NULL families
# (SYNTHETIC; true pi0 = 1 by construction, so any pi0-hat < 1 is estimation error
# and any q < 0.05 discovery is a false positive).
suppressMessages(library(qvalue))
set.seed(20260916)
REPS <- 500
cat(sprintf('%6s %9s %9s %9s %9s %12s %14s\n', 'm', 'med pi0', 'min pi0',
            'p05 pi0', 'errors', 'reps w/ FD', 'mean FD (q<.05)'))
for (m in c(20, 50, 100, 200, 1000, 5000, 20000)) {
  pi0s <- numeric(0); fds <- numeric(0); errs <- 0
  for (r in seq_len(REPS)) {
    pv <- runif(m)                       # ALL NULL
    o <- try(qvalue(pv), silent = TRUE)
    if (inherits(o, 'try-error')) { errs <- errs + 1; next }
    pi0s <- c(pi0s, o$pi0)
    fds  <- c(fds, sum(o$qvalues < 0.05))
  }
  cat(sprintf('%6d %9.3f %9.3f %9.3f %9d %12.3f %14.3f\n', m,
              median(pi0s), min(pi0s), quantile(pi0s, 0.05), errs,
              mean(fds > 0), mean(fds)))
}
cat('\nSame families under plain BH (which needs no pi0 estimate):\n')
set.seed(20260916)
for (m in c(20, 50, 100, 200, 1000, 5000, 20000)) {
  fds <- replicate(REPS, sum(p.adjust(runif(m), 'BH') < 0.05))
  cat(sprintf('m=%6d  reps with >=1 false discovery: %.3f   mean false discoveries: %.3f\n',
              m, mean(fds > 0), mean(fds)))
}
