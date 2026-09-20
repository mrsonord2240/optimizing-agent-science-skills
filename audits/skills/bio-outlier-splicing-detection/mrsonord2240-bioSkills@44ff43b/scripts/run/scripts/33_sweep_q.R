# q / implementation sweep on the counted synthetic cohort (FRASER in as-drop = 2.6.1). Tests SKILL.md hyperparameter claims.
suppressPackageStartupMessages({library(FRASER); library(BiocParallel)})
a <- commandArgs(TRUE); wd <- a[1]; synth <- a[2]
source(file.path(dirname(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE))), "20_eval_lib.R"))
bp <- MulticoreParam(12)
fds0 <- loadFraserDataSet(dir = wd, name = "rare_disease_cohort")
fds0 <- calculatePSIValues(fds0)
fds0 <- filterExpressionAndVariability(fds0, minDeltaPsi = 0.0, minExpressionInOneSample = 20, quantile = 0.05, quantileMinExpression = 1)
fitMetrics(fds0) <- 'jaccard'; currentType(fds0) <- 'jaccard'
cat("junctions after Skill's filter:", nrow(fds0), "\n")
# --- Skill claim: estimateBestQ(fds, type='jaccard', useOHT=TRUE) then bestQ(fds)
t0 <- Sys.time()
fdsq <- estimateBestQ(fds0, type = "jaccard", useOHT = TRUE)
cat("OHT estimateBestQ done; bestQ(fds,'jaccard') =", bestQ(fdsq, "jaccard"), " (", round(as.numeric(Sys.time() - t0, units = "secs")), "s)\n")
qbest <- bestQ(fdsq, "jaccard")
for (q in c()) {
  f <- suppressWarnings(FRASER(fds0, q = c(jaccard = q), BPPARAM = bp)); eval_fds(f, synth, tag = paste0("PCA q=", q))
}
for (qq in c(qbest, 5, 10)) tryCatch({ f <- suppressWarnings(FRASER(fds0, q = c(jaccard = qq), correction = "AE", BPPARAM = bp)); eval_fds(f, synth, tag = paste0("AE q=", qq)) }, error = function(e) cat("AE q=", qq, "FAILED:", conditionMessage(e), "
"))
# --- Skill claim: exhaustive search with useOHT=FALSE + plotEncDimSearch
t0 <- Sys.time()
fdse <- tryCatch(estimateBestQ(fds0, type = "jaccard", useOHT = FALSE, q_param = c(2, 5, 10, 15, 20), BPPARAM = bp), error = function(e) { cat("useOHT=FALSE FAILED:", conditionMessage(e), "\n"); NULL })
if (!is.null(fdse)) {
  cat("exhaustive: bestQ =", bestQ(fdse, "jaccard"), " (", round(as.numeric(Sys.time() - t0, units = "secs")), "s)\n")
  pdf(file.path(wd, "encdim.pdf")); pl <- tryCatch(plotEncDimSearch(fdse, type = "jaccard"), error = function(e) { cat("plotEncDimSearch FAILED:", conditionMessage(e), "\n"); NULL }); print(pl); dev.off()
  if (!is.null(pl)) cat("plotEncDimSearch produced object of class", class(pl)[1], "\n")
}
