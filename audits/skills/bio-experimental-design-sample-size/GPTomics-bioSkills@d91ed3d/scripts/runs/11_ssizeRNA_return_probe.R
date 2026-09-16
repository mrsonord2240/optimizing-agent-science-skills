# Probe: what does ssizeRNA actually return, and is the SKILL.md line
#   res$ssize   # minimum n per group
# a correct description of the contract?  Also: does the NA come from maxN being too small?
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
pdf(NULL)
suppressPackageStartupMessages(library(ssizeRNA))

probe <- function(lbl, ...) {
  set.seed(99)
  r <- tryCatch(ssizeRNA_single(...), error = function(e) paste("ERROR:", conditionMessage(e)))
  cat("\n### ", lbl, "\n")
  if (!is.list(r)) { cat("   ", r, "\n"); return(invisible(NULL)) }
  cat("   names(res):", paste(names(r), collapse = ", "), "\n")
  cat("   res$ssize  =", paste(names(r$ssize), signif(r$ssize, 4), collapse = " | "), "\n")
  cat("   length(res$ssize) =", length(r$ssize), "  class:", class(r$ssize), "\n")
  if (!is.null(r$power)) {
    pw <- r$power
    cat("   power table (first col = n): \n")
    print(utils::head(pw, 40))
  }
  invisible(r)
}

probe("mu=10 disp=0.2 fc=1.5 maxN=30  (SKILL.md canonical parameters)",
      nGenes = 20000, pi0 = 0.95, m = 200, mu = 10, disp = 0.2,
      fc = 1.5, fdr = 0.05, power = 0.80, maxN = 30)

probe("mu=10 disp=0.2 fc=1.5 maxN=200 (same, larger search range)",
      nGenes = 20000, pi0 = 0.95, m = 200, mu = 10, disp = 0.2,
      fc = 1.5, fdr = 0.05, power = 0.80, maxN = 200)

probe("mu=100 disp=0.2 fc=1.5 maxN=30 (realistic mean count)",
      nGenes = 20000, pi0 = 0.95, m = 200, mu = 100, disp = 0.2,
      fc = 1.5, fdr = 0.05, power = 0.80, maxN = 30)

probe("mu=100 disp=0.2 fc=2.0 maxN=30 (larger effect)",
      nGenes = 20000, pi0 = 0.95, m = 200, mu = 100, disp = 0.2,
      fc = 2.0, fdr = 0.05, power = 0.80, maxN = 30)
