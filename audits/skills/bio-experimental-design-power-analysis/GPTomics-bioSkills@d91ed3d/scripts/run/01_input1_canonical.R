# Input 1 -- Canonical: "I'm comparing drug-treated versus control cells, expect biological CV
# around 0.3, and want to detect 1.5-fold changes. How many replicates for 80% power, and can you
# confirm with simulation?"
# Exercises the SKILL.md "Closed-Form NB Power -- RNASeqPower" block, then confirms with the
# SKILL.md "Simulation-Based Power" PROPER block (reduced nsims for a short audit run; the trend,
# not the exact decimal, is what is being checked).

suppressPackageStartupMessages(library(RNASeqPower))

cat("=== A. Closed-form (SKILL.md pattern), CV=0.3, 1.5-fold, depth=20 ===\n")
n_needed <- rnapower(depth = 20, cv = 0.3, effect = 1.5, alpha = 0.05, power = 0.80)
cat("raw n solve:", n_needed, " ceiling:", ceiling(n_needed), "\n")

cat("\nPower at n=3,4,...,10 (CV=0.3, 1.5-fold, depth=20):\n")
for (n in 3:10) {
  p <- rnapower(depth = 20, n = n, cv = 0.3, effect = 1.5, alpha = 0.05)
  cat(sprintf("  n=%2d  power=%.4f\n", n, p))
}

cat("\n=== B. Simulation-based marginal power (PROPER), reduced nsims for a short audit run ===\n")
if (requireNamespace("PROPER", quietly = TRUE)) {
  suppressPackageStartupMessages(library(PROPER))
  set.seed(42)
  sim_opts <- RNAseq.SimOptions.2grp(ngenes = 5000, p.DE = 0.05,
                                     lOD = "cheung", lBaselineExpr = "cheung")
  sims <- runSims(Nreps = c(3, 5, 8, 12), sim.opts = sim_opts, nsims = 15, DEmethod = "edgeR")
  powr <- comparePower(sims, alpha.type = "fdr", alpha.nominal = 0.05,
                       stratify.by = "expr", delta = log(1.5))
  sp <- summaryPower(powr)
  print(sp)
  cat("\nmarginal power by Nreps (column 'marginal power' if present):\n")
  print(colnames(sp))
} else {
  cat("PROPER not available\n")
}
