suppressPackageStartupMessages(library(ssizeRNA))
set.seed(20260923)
res <- ssizeRNA_single(nGenes = 20000, pi0 = 0.95, m = 200, mu = 200, disp = 0.2,
                       fc = 1.5, fdr = 0.05, power = 0.80, maxN = 200)
n <- res$ssize[, "ssize"]
stopifnot(length(n) == 1L, is.finite(n), n >= 2, n <= 200)
cat(sprintf("OK scalar n=%d power=%.3f\n", n, res$ssize[, "power"]))
