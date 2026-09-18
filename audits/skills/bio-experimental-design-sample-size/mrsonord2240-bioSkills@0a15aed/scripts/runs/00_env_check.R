cat("R version:", R.version.string, "\n")
for (p in c("ssizeRNA","PROPER","DESeq2","edgeR","pwr")) {
  v <- tryCatch(as.character(packageVersion(p)), error=function(e) "MISSING")
  cat(p, ":", v, "\n")
}
