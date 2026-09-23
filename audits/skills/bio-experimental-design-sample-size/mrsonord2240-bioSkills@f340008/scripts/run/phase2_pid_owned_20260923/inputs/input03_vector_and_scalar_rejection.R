library(ssizeRNA)
set.seed(20260923)
mu_vec <- exp(seq(log(50), log(600), length.out = 300))
disp_vec <- pmax(0.08, 0.35 - 0.04 * log10(mu_vec / 50))
res <- ssizeRNA_vary(nGenes = length(mu_vec), pi0 = 0.95, mu = mu_vec,
                     disp = disp_vec, fc = 1.5, fdr = 0.05,
                     power = 0.80, maxN = 200)
n <- res$ssize[, "ssize"]
stopifnot(is.finite(n), n >= 2, n <= 200, is.finite(res$ssize[, "power"]))
scalar_error <- tryCatch({
  ssizeRNA_vary(nGenes = 20000, pi0 = 0.95, mu = 200, disp = 0.2,
                 fc = 1.5, fdr = 0.05, power = 0.80, maxN = 20)
  NULL
}, error = function(e) conditionMessage(e))
stopifnot(!is.null(scalar_error), grepl("non-finite|integrate", scalar_error, ignore.case = TRUE))
cat(sprintf("OK vectors: n=%d achieved_power=%.3f; scalar _vary rejected: %s\n",
            n, res$ssize[, "power"], scalar_error))
