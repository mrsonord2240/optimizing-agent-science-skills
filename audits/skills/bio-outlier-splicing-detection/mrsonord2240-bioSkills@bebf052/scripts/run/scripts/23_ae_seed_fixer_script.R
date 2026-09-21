suppressPackageStartupMessages({library(FRASER); library(BiocParallel)})
a <- commandArgs(TRUE); wd <- a[1]
fds0 <- loadFraserDataSet(dir = wd, name = "rare_disease_cohort")
cat("FRASER", as.character(packageVersion("FRASER")), "\n")
fitp <- function(seed) { if (!is.na(seed)) set.seed(seed)
  f <- FRASER(fds0, q = c(jaccard = 5), implementation = "AE", iterations = 5, BPPARAM = SerialParam(RNGseed = if (is.na(seed)) NULL else seed))
  pVals(f, type = "jaccard", level = "site") }
t0 <- Sys.time()
p1 <- fitp(1); p2 <- fitp(1); p3 <- fitp(NA); p4 <- fitp(NA)
d <- function(x, y) sprintf("max|dP|=%.3g, cells |dP|>1e-6: %d of %d", max(abs(as.matrix(x) - as.matrix(y)), na.rm = TRUE), sum(abs(as.matrix(x) - as.matrix(y)) > 1e-6, na.rm = TRUE), length(x))
cat("set.seed(1) twice :", d(p1, p2), "\n")
cat("no seed twice     :", d(p3, p4), "\n")
cat("secs", as.numeric(Sys.time() - t0, units = "secs"), "\n")
