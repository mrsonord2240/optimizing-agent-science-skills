for (p in c("BiocManager", "remotes", "DESeq2")) {
  cat(p, requireNamespace(p, quietly = TRUE), "\n")
}
