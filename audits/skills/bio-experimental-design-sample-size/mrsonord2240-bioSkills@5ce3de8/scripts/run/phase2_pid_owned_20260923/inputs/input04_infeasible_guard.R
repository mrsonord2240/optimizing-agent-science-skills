library(ssizeRNA)
set.seed(20260923)
res <- ssizeRNA_single(nGenes = 20000, pi0 = 0.99, m = 100,
                       mu = 5, disp = 2, fc = 1.1, fdr = 0.01,
                       power = 0.95, maxN = 2)
n <- res$ssize[, "ssize"]
stopifnot(is.na(n))
guard_message <- tryCatch({
  if (is.na(n)) stop("no n <= maxN reaches the target; raise maxN or revise fc/dispersion")
  "unexpected success"
}, error = function(e) conditionMessage(e))
stopifnot(grepl("no n <= maxN", guard_message, fixed = TRUE))
cat(sprintf("OK infeasible guard: ssize=NA and guard message=%s\n", guard_message))
