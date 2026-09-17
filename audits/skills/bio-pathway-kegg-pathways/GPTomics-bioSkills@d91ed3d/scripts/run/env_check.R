cat("R version:", R.version.string, "\n")
for (p in c("clusterProfiler","org.Hs.eg.db","gson","SPIA","graphite","pathview","KEGGREST","enrichplot")) {
  ok <- requireNamespace(p, quietly=TRUE)
  cat(p, ok, if(ok) as.character(packageVersion(p)) else "MISSING", "\n")
}
