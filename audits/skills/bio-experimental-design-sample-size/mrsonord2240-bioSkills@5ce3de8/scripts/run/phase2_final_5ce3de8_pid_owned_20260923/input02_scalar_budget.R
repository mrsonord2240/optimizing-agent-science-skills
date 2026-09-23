suppressPackageStartupMessages(library(ssizeRNA))
set.seed(20260923)
res <- ssizeRNA_single(nGenes = 20000, pi0 = 0.95, m = 200, mu = 200, disp = 0.2,
                       fc = 1.5, fdr = 0.05, power = 0.80, maxN = 200)
n <- res$ssize[, "ssize"]
stopifnot(length(n) == 1L, is.finite(n), n >= 2, n <= 200)
cp <- check.power(nGenes = 20000, pi0 = 0.95, m = 6, mu = 200, disp = 0.2,
                  fc = 1.5, fdr = 0.05, sims = 20)
stopifnot(is.finite(cp$pow_bh_ave), is.nan(cp$fdr_bh_ave) || is.finite(cp$fdr_bh_ave))
cat(sprintf("OK scalar n=%d achieved_power=%.3f; fixed_n_power=%.3f true_fdr=%s\n",
            n, res$ssize[, "power"], cp$pow_bh_ave,
            if (is.nan(cp$fdr_bh_ave)) "NaN_zero_discoveries" else sprintf("%.3f", cp$fdr_bh_ave)))
