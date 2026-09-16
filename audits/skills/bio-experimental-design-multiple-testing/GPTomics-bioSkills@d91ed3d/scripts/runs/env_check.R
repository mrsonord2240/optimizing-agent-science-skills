.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
cat("R version:", R.version.string, "\n")
for (p in c("qvalue","IHW","limma","DESeq2","edgeR")) {
  ok <- requireNamespace(p, quietly=TRUE)
  cat(sprintf("%-8s installed=%s version=%s\n", p, ok, if(ok) as.character(packageVersion(p)) else "NA"))
}
cat("p.adjust methods:", paste(p.adjust.methods, collapse=", "), "\n")
