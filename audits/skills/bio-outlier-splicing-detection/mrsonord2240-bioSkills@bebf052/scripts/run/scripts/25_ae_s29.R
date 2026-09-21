# Tissue-mismatch claim on FRASER 2.6.1: calls in the shifted sample S29 with PCA (default) vs AE q=10, two AE fits each with the Skill's block-08 check
suppressPackageStartupMessages({library(FRASER); library(BiocParallel)})
fds0 <- loadFraserDataSet(dir = commandArgs(TRUE)[1], name = "rare_disease_cohort")
fitMetrics(fds0) <- "jaccard"; currentType(fds0) <- "jaccard"
for (impl in c("PCA", "AE", "AE")) {
  q <- if (impl == "PCA") 5 else 10
  fds <- suppressWarnings(FRASER(fds0, q = c(jaccard = q), implementation = impl, BPPARAM = SerialParam(RNGseed = 1)))
  all_results <- as.data.frame(results(fds, psiType = "jaccard", padjCutoff = 0.05, deltaPsiCutoff = 0.1))
  cat(sprintf("== %s q=%d: total calls %d; S29 calls %d\n", impl, q, nrow(all_results), sum(all_results$sampleID == "S29")))
  print(sort(table(factor(all_results$sampleID, levels = colnames(fds))), decreasing = TRUE)[1:5])   # SKILL.md block 08
}
