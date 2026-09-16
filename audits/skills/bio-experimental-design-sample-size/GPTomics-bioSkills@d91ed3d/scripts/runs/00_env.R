.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
cat("R version:", R.version.string, "\n")
for (p in c("ssizeRNA","PROPER","RNASeqPower","pwr","DESeq2","edgeR","limma","powsimR","Biobase","qvalue")) {
  v <- tryCatch(as.character(packageVersion(p)), error=function(e) "MISSING")
  cat(sprintf("%-14s %s\n", p, v))
}
cat("\n--- ssizeRNA exports ---\n"); print(ls("package:ssizeRNA"))
suppressPackageStartupMessages(library(ssizeRNA))
cat("\n--- args(ssizeRNA_single) ---\n"); print(args(ssizeRNA_single))
cat("\n--- args(ssizeRNA_vary) ---\n");  print(args(ssizeRNA_vary))
cat("\n--- args(check.power) ---\n");    print(args(check.power))
