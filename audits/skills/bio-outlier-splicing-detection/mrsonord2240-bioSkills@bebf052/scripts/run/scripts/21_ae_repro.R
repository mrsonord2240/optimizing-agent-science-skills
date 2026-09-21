# Check SKILL.md "Reproducibility" claim on FRASER 2.6.1, from the fds saved by the shipped example (ex_drop/fraser_workdir).
# All fits SerialParam (MulticoreParam workers were killed on the loaded machine: 'error writing to connection', see logs/17).
suppressPackageStartupMessages({library(FRASER); library(BiocParallel)})
fds0 <- loadFraserDataSet(dir = commandArgs(TRUE)[1], name = "rare_disease_cohort")
fitMetrics(fds0) <- "jaccard"; currentType(fds0) <- "jaccard"
cat("loaded", nrow(fds0), "junctions x", ncol(fds0), "samples\n")
fit <- function(bp, impl = "AE", seed = NULL) { if (!is.null(seed)) set.seed(seed)
  f <- suppressWarnings(FRASER(fds0, q = c(jaccard = 5), implementation = impl, BPPARAM = bp)); pVals(f, type = "jaccard") }
nd <- function(x, y) sum(abs(x - y) > 1e-6, na.rm = TRUE)
a1 <- fit(SerialParam()); a2 <- fit(SerialParam()); cat("AE, no seed, SerialParam():          cells differing >1e-6:", nd(a1, a2), "of", length(a1), "\n")
b1 <- fit(SerialParam(), seed = 1); b2 <- fit(SerialParam(), seed = 1); cat("AE, set.seed(1), SerialParam():      cells differing:", nd(b1, b2), "\n")
c1 <- fit(SerialParam(RNGseed = 1)); c2 <- fit(SerialParam(RNGseed = 1)); cat("AE, SerialParam(RNGseed = 1):        cells differing:", nd(c1, c2), "\n")
p1 <- fit(SerialParam(), impl = "PCA"); p2 <- fit(SerialParam(), impl = "PCA"); cat("PCA q=5 twice:                       cells differing:", nd(p1, p2), "\n")
