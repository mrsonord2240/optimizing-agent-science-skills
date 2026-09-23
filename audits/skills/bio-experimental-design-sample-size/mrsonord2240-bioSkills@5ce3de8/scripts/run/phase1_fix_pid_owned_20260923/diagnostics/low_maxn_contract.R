suppressPackageStartupMessages(library(ssizeRNA))
safe_ssize <- function(call) {
  tryCatch(call(), error = function(e) {
    if (identical(conditionMessage(e), "argument is of length zero")) return(NULL)
    stop(e)
  })
}
require_reachable_n <- function(res, maxN) {
  n <- if (is.null(res)) NA_real_ else res$ssize[, "ssize"]
  if (length(n) != 1L || is.na(n)) {
    stop(sprintf("no n <= %d reaches the target; raise maxN or revise fc/dispersion", maxN))
  }
  n
}
result <- tryCatch({
  res <- safe_ssize(function() ssizeRNA_single(nGenes = 20000, pi0 = 0.95, m = 200,
                                                mu = 200, disp = 0.2, fc = 1.5, fdr = 0.05,
                                                power = 0.80, maxN = 2))
  require_reachable_n(res, maxN = 2)
  "unexpected-success"
}, error = conditionMessage)
stopifnot(identical(result, "no n <= 2 reaches the target; raise maxN or revise fc/dispersion"))
cat("OK low-maxN emits documented unreachable message\n")
