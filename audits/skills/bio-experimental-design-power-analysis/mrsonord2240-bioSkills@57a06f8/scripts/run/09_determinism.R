suppressPackageStartupMessages(library(PROPER))
one <- function() {
  opt <- RNAseq.SimOptions.2grp(ngenes = 500, p.DE = .05, lOD = "cheung", lBaselineExpr = "cheung")
  sims <- runSims(Nreps = c(3, 6), sim.opts = opt, nsims = 2, DEmethod = "edgeR")
  summaryPower(comparePower(sims, alpha.type = "fdr", alpha.nominal = .05, stratify.by = "expr", delta = log(1.5)))
}
a <- one(); b <- one()
stopifnot(identical(a, b))
print(a)
cat("DETERMINISM_ASSERTION=PASS\n")
