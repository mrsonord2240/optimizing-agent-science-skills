cat("R version:", R.version.string, "\n")
for (p in c("clusterProfiler","fgsea","org.Hs.eg.db","msigdbr","ReactomePA","reactome.db","GSVA","limma","DOSE")) {
  cat(sprintf("%-15s %s\n", p, as.character(packageVersion(p))))
}
