# T3 / 8.4 determinism check: run the identical SKILL.md PROPER block twice with NO seed set
# (as SKILL.md and examples/rnaseq_power.R both do -- neither calls set.seed anywhere) and compare.
suppressPackageStartupMessages({ library(RNASeqPower); library(PROPER) })

run_once <- function() {
  sim_opts <- RNAseq.SimOptions.2grp(ngenes = 3000, p.DE = 0.05, lOD = "cheung", lBaselineExpr = "cheung")
  sims <- runSims(Nreps = c(3, 8), sim.opts = sim_opts, nsims = 10, DEmethod = "edgeR")
  powr <- comparePower(sims, alpha.type = "fdr", alpha.nominal = 0.05, stratify.by = "expr", delta = log(1.5))
  summaryPower(powr)[, "Marginal power"]
}

cat("closed-form rnapower (deterministic, no RNG): repeated 3x ->\n")
for (i in 1:3) cat(" ", rnapower(depth = 20, n = 5, cv = 0.4, effect = 2, alpha = 0.05), "\n")

cat("\nPROPER simulation marginal power at Nreps=c(3,8), unseeded, repeated 4x:\n")
invisible(capture.output(res <- replicate(4, run_once())))
print(t(res))
cat("range at Nreps=3:", range(res[1,]), "  range at Nreps=8:", range(res[2,]), "\n")
