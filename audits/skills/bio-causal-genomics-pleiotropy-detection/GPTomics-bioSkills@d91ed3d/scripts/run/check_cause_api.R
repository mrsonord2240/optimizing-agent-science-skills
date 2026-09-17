if (requireNamespace("cause", quietly=TRUE)) {
  cat("cause IS installed:", as.character(packageVersion("cause")), "\n")
} else {
  cat("cause NOT installed (expected per TOOLS.md)\n")
}
if (requireNamespace("lhcMR", quietly=TRUE)) {
  cat("lhcMR IS installed\n")
} else {
  cat("lhcMR NOT installed (expected)\n")
}
# Check mrclust's documented function signature vs what SKILL.md shows
library(mrclust)
print(args(mr_clust_em))
