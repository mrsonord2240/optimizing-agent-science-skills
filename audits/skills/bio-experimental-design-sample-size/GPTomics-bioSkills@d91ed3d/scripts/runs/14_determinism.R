# T3 (Result Determinism) evidence. The SKILL.md code blocks contain NO set.seed, and both
# ssizeRNA entry points are simulation-based. Does the recommended n move between calls?
# Uses parameters that actually return a number (mu=100, fc=2.0, maxN=30).
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
pdf(NULL)
suppressPackageStartupMessages(library(ssizeRNA))
cat("--- ssizeRNA_single, NO seed, 8 consecutive calls (mu=100 disp=0.2 fc=2.0 fdr=.05 power=.80) ---\n")
ns <- c()
for (i in 1:8) {
  r <- ssizeRNA_single(nGenes = 20000, pi0 = 0.95, m = 200, mu = 100, disp = 0.2,
                       fc = 2.0, fdr = 0.05, power = 0.80, maxN = 30)
  n <- as.vector(r$ssize)[2]; ns <- c(ns, n)
  cat(sprintf("   call %d: n = %s\n", i, n)); flush.console()
}
cat(sprintf("   -> distinct values: %s ; range %s-%s ; sd %.2f\n",
            paste(sort(unique(ns)), collapse = ","), min(ns), max(ns), sd(ns)))

cat("\n--- check.power, NO seed, 5 consecutive calls (m=6, mu=100, disp=0.2, fc=2.0, sims=20) ---\n")
pw <- c()
for (i in 1:5) {
  cp <- check.power(nGenes = 20000, pi0 = 0.95, m = 6, mu = 100, disp = 0.2,
                    fc = 2.0, fdr = 0.05, sims = 20)
  pw <- c(pw, cp$pow_bh_ave)
  cat(sprintf("   call %d: BH average power = %.4f, true FDR = %.4f\n", i, cp$pow_bh_ave, cp$fdr_bh_ave))
  flush.console()
}
cat(sprintf("   -> power range %.4f-%.4f (spread %.4f)\n", min(pw), max(pw), max(pw) - min(pw)))
