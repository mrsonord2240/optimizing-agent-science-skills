# Input 1 (Canonical) -- runs the SKILL.md "FDR-Aware NB Sample Size -- ssizeRNA" snippet VERBATIM.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
pdf(NULL)  # suppress Rplots.pdf side effect from ssize.twoSampVary's power-curve plot

library(ssizeRNA)

cat("=== A. SKILL.md snippet verbatim, repeated 5x (no set.seed in the SKILL.md snippet) ===\n")
t0 <- Sys.time()
ns <- numeric(0)
for (i in 1:5) {
  res <- ssizeRNA_vary(nGenes = 20000, pi0 = 0.95,        # 5% DE
                       mu = 10, disp = 0.2,                # mean count + dispersion (from pilot ideally)
                       fc = 1.5, fdr = 0.05, power = 0.80,
                       maxN = 30)
  ns <- c(ns, res$ssize)
  cat(sprintf("  run %d: res$ssize = %s   (class %s, names: %s)\n", i, res$ssize,
              class(res$ssize), paste(names(res), collapse=",")))
}
cat(sprintf("  -> distinct n across 5 unseeded runs: %s\n", paste(sort(unique(ns)), collapse=", ")))
cat(sprintf("  elapsed: %.1f s\n", as.numeric(difftime(Sys.time(), t0, units="secs"))))

cat("\n=== B. Is ssizeRNA_vary with SCALAR mu/disp any different from ssizeRNA_single? ===\n")
set.seed(101); v <- ssizeRNA_vary  (nGenes=20000, pi0=0.95, m=200, mu=10, disp=0.2, fc=1.5, fdr=0.05, power=0.80, maxN=30)$ssize
set.seed(101); s <- ssizeRNA_single(nGenes=20000, pi0=0.95, m=200, mu=10, disp=0.2, fc=1.5, fdr=0.05, power=0.80, maxN=30)$ssize
cat(sprintf("  same seed, scalar mu/disp:  ssizeRNA_vary n=%s   ssizeRNA_single n=%s\n", v, s))
cat(sprintf("  identical function bodies? %s\n", identical(deparse(body(ssizeRNA_vary)), deparse(body(ssizeRNA_single)))))

cat("\n=== C. check.power at the recommended n (SKILL.md snippet, line 2) ===\n")
set.seed(20260916)
cp <- check.power(nGenes = 20000, pi0 = 0.95, m = 6, mu = 10, disp = 0.2, fc = 1.5, fdr = 0.05, sims = 50)
cat("  names(check.power output):", paste(names(cp), collapse=", "), "\n")
for (nm in names(cp)) cat(sprintf("    %-14s %s\n", nm, paste(signif(unlist(cp[[nm]]),4), collapse=" ")))
saveRDS(list(ns=ns, cp=cp), "runs/01_input1.rds")
