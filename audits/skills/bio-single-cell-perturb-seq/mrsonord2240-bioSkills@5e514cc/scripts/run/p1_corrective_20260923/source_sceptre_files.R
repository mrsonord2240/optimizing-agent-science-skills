.libPaths(c("F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib", .libPaths()))
library(methods)
source_dir <- "F:/OpenScience/audits/bio-single-cell-perturb-seq/run/p1_corrective_20260923/sceptre-source/R"
env <- new.env(parent = globalenv())
for (f in list.files(source_dir, full.names = TRUE, pattern = "\\.R$")) {
  cat("SOURCING ", basename(f), "\n", sep = "")
  sys.source(f, envir = env)
}
cat("PASS sourced ", length(ls(env)), " bindings\n", sep = "")
