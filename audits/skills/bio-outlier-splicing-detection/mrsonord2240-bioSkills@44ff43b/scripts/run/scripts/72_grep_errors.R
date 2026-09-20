# Are the Skill's "Common Errors" messages real? Search every function body in FRASER/OUTRIDER for the quoted strings.
suppressPackageStartupMessages({library(FRASER); library(OUTRIDER)})
pats <- c("cohort too small", "too small", "convergence not reached", "not reached", "encoding-dim search", "countRNAData failed")
for (pkg in c("FRASER", "OUTRIDER")) {
  ns <- asNamespace(pkg); hits <- list()
  for (nm in ls(ns, all.names = TRUE)) { f <- get(nm, ns); if (is.function(f)) { txt <- paste(deparse(f), collapse = "\n"); for (p in pats) if (grepl(p, txt, fixed = TRUE)) hits[[length(hits) + 1]] <- paste(p, "in", nm) } }
  cat(pkg, as.character(packageVersion(pkg)), ": matches ->", if (length(hits)) paste(unlist(hits), collapse = "; ") else "NONE", "\n")
}
