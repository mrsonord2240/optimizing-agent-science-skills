# Which factor made the fixer's AE fits reproducible? (its script: set.seed(1) + SerialParam(RNGseed=1) + iterations=5 -> 0 differ; audit run 21: default iterations, either seed alone -> ~9.3-9.8k differ)
suppressPackageStartupMessages({library(FRASER); library(BiocParallel)})
fds0 <- loadFraserDataSet(dir = commandArgs(TRUE)[1], name = "rare_disease_cohort")
fitMetrics(fds0) <- "jaccard"; currentType(fds0) <- "jaccard"
fit <- function(iter, both, rngseed = TRUE) { if (both) set.seed(1)
  f <- suppressWarnings(FRASER(fds0, q = c(jaccard = 5), implementation = "AE", iterations = iter, BPPARAM = if (rngseed) SerialParam(RNGseed = 1) else SerialParam())); pVals(f, type = "jaccard") }
nd <- function(x, y) sum(abs(x - y) > 1e-6, na.rm = TRUE)
for (cfg in list(list(iter = 5, both = FALSE, rng = TRUE, lab = "iterations=5, RNGseed=1 only"),
                 list(iter = 15, both = TRUE, rng = TRUE, lab = "iterations=15 (default), set.seed(1) + RNGseed=1"),
                 list(iter = 5, both = TRUE, rng = FALSE, lab = "iterations=5, set.seed(1) only"))) {
  a <- fit(cfg$iter, cfg$both, cfg$rng); b <- fit(cfg$iter, cfg$both, cfg$rng)
  cat(sprintf("FACTOR %-52s cells differing >1e-6: %d of %d\n", cfg$lab, nd(a, b), length(a)))
}
