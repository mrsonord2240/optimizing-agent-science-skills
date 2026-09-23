cat(R.version.string, "\n")
for (p in c("DESeq2", "ssizeRNA", "PROPER", "pwr")) {
  cat(p, requireNamespace(p, quietly = TRUE), "\n")
}
