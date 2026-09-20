suppressPackageStartupMessages({library(FRASER); library(BiocParallel)})
fds0 <- loadFraserDataSet(dir = "ex_drop/wf_q10", name = "rare_disease_cohort"); fds0 <- calculatePSIValues(fds0)
fds0 <- filterExpressionAndVariability(fds0, minDeltaPsi = 0.0, minExpressionInOneSample = 20, quantile = 0.05, quantileMinExpression = 1)
fitMetrics(fds0) <- "jaccard"; currentType(fds0) <- "jaccard"
p <- lapply(1:2, function(i) { f <- suppressWarnings(FRASER(fds0, q = c(jaccard = 5), correction = "AE", BPPARAM = MulticoreParam(8))); as.matrix(pVals(f, type = "jaccard", level = "site", filters = FALSE)) })
d <- abs(p[[1]] - p[[2]]); cat("FRASER AE q=5 (no seed): max |dP| =", max(d, na.rm = TRUE), "; cells with |dP|>1e-6:", sum(d > 1e-6, na.rm = TRUE), "of", sum(!is.na(d)), "; cells p<0.001 run1:", sum(p[[1]] < 1e-3, na.rm = TRUE), " run2:", sum(p[[2]] < 1e-3, na.rm = TRUE), " both:", sum(p[[1]] < 1e-3 & p[[2]] < 1e-3, na.rm = TRUE), "\n")
