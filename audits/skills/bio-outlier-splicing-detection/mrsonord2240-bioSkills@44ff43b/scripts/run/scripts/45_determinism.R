# T3 (result determinism): repeat fits on identical input, compare p-value matrices. as-drop: FRASER 2.6.1, OUTRIDER 1.28.1
suppressPackageStartupMessages({library(FRASER); library(OUTRIDER); library(BiocParallel)})
cnt <- read.table("data/outrider/counts.tsv", header = TRUE, row.names = 1)
ods0 <- OutriderDataSet(countData = cnt); ods0 <- filterExpression(ods0, minCounts = TRUE, filterGenes = TRUE)
r <- lapply(1:2, function(i) { o <- suppressWarnings(OUTRIDER(ods0, q = 8, BPPARAM = SerialParam())); assay(o, "pValue") })
cat("OUTRIDER (AE, q=8, no seed set) run1 vs run2: max |dP| =", max(abs(r[[1]] - r[[2]])), "; max |dlog10 P| =", max(abs(log10(r[[1]]) - log10(r[[2]])), na.rm = TRUE), "\n")
fds0 <- loadFraserDataSet(dir = "ex_drop/wf_q10", name = "rare_disease_cohort"); fds0 <- calculatePSIValues(fds0)
fds0 <- filterExpressionAndVariability(fds0, minDeltaPsi = 0.0, minExpressionInOneSample = 20, quantile = 0.05, quantileMinExpression = 1)
fitMetrics(fds0) <- "jaccard"; currentType(fds0) <- "jaccard"
for (corr in c("PCA", "AE")) {
  p <- lapply(1:2, function(i) { f <- suppressWarnings(FRASER(fds0, q = c(jaccard = 5), correction = corr, BPPARAM = MulticoreParam(8))); pVals(f, type = "jaccard", level = "site", filters = FALSE) })
  cat("FRASER", corr, "q=5 run1 vs run2: max |dlog10 P| =", max(abs(log10(as.matrix(p[[1]])) - log10(as.matrix(p[[2]]))), na.rm = TRUE), "\n")
}
