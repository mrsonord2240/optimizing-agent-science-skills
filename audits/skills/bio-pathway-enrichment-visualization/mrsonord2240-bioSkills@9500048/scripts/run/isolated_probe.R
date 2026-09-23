cat("R=", R.version.string, "\n", sep = "")
cat("BiocManager=", requireNamespace("BiocManager", quietly = TRUE), "\n", sep = "")
for (pkg in c("clusterProfiler", "enrichplot", "org.Hs.eg.db", "GOSemSim", "ggplot2", "ggridges", "ggarchery", "ggupset")) {
  cat(pkg, "=", if (requireNamespace(pkg, quietly = TRUE)) as.character(packageVersion(pkg)) else "MISSING", "\n", sep = "")
}
