.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
pdf(NULL)
library(ssizeRNA)
try_n <- function(lbl, expr) {
  r <- tryCatch(eval(expr), error=function(e) paste("ERROR:", conditionMessage(e)))
  if (is.list(r)) cat(sprintf("%-46s n=%s\n", lbl, r$ssize)) else cat(sprintf("%-46s %s\n", lbl, r))
}
cat("--- SKILL.md snippet (vary, scalars, mu=10 disp=0.2), 8 unseeded reps ---\n")
for (i in 1:8) try_n(sprintf("  vary mu=10 disp=0.2 rep%d", i),
  quote(ssizeRNA_vary(nGenes=20000, pi0=0.95, mu=10, disp=0.2, fc=1.5, fdr=0.05, power=0.80, maxN=30)))

cat("\n--- examples/sample_size_estimation.R snippet (single, m=200, mu=10 disp=0.2, seeded 20260528) ---\n")
set.seed(20260528)
try_n("  single mu=10 disp=0.2 (example script)",
  quote(ssizeRNA_single(nGenes=20000, pi0=0.95, m=200, mu=10, disp=0.2, fc=1.5, fdr=0.05, power=0.80, maxN=30)))

cat("\n--- sensitivity: does mean count drive the failure? (vary, scalars, seeded) ---\n")
for (mu in c(10, 25, 50, 100, 500)) {
  set.seed(7)
  try_n(sprintf("  vary mu=%-4g disp=0.2", mu),
    quote(ssizeRNA_vary(nGenes=20000, pi0=0.95, mu=mu, disp=0.2, fc=1.5, fdr=0.05, power=0.80, maxN=30)))
}
cat("\n--- sensitivity: nGenes / pi0 ---\n")
for (ng in c(5000, 10000, 20000)) { set.seed(7)
  try_n(sprintf("  vary nGenes=%-6d mu=10", ng),
    quote(ssizeRNA_vary(nGenes=ng, pi0=0.95, mu=10, disp=0.2, fc=1.5, fdr=0.05, power=0.80, maxN=30))) }
