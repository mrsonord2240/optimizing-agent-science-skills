for (p in c("edgeR", "limma", "qvalue", "Biobase", "ssize.fdr", "MASS")) {
  cat(p, requireNamespace(p, quietly = TRUE), "\n")
}

