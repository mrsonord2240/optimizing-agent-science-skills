# Definitive A/B for the SKILL.md defect: ssizeRNA_vary with SCALAR mu/disp (exactly as the
# SKILL.md code block writes it) vs the SAME call with per-gene VECTORS, same seed.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
pdf(NULL)
suppressPackageStartupMessages(library(ssizeRNA))
NG <- 5000
show <- function(lbl, mu, disp) {
  set.seed(2026)
  r <- tryCatch(ssizeRNA_vary(nGenes = NG, pi0 = 0.95, m = 200, mu = mu, disp = disp,
                              fc = 1.5, fdr = 0.05, power = 0.80, maxN = 30),
                error = function(e) paste("ERROR:", conditionMessage(e)))
  if (is.list(r)) cat(sprintf("%-52s -> ssize row: %s\n", lbl,
                              paste(names(r$ssize), signif(as.vector(r$ssize), 4), collapse = " ")))
  else cat(sprintf("%-52s -> %s\n", lbl, r))
}
show("ssizeRNA_vary(mu=100, disp=0.2)      [SKILL.md form]", 100, 0.2)
show("ssizeRNA_vary(mu=rep(100,nGenes), disp=rep(0.2,nGenes))",
     rep(100, NG), rep(0.2, NG))
show("ssizeRNA_vary(mu=100, disp=rep(0.2,nGenes))", 100, rep(0.2, NG))
show("ssizeRNA_vary(mu=rep(100,nGenes), disp=0.2)", rep(100, NG), 0.2)
