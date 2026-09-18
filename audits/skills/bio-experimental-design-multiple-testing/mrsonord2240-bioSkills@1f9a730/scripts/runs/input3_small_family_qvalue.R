# Input 3 (Edge, regression of pre-fix Input 3 + independent verification of the fix's
# claimed lambda=0 fallback and the fixer's claim that pi0.method='bootstrap' does NOT fix it).
# All-null families of size m = 10 (new, more extreme than the pre-fix audit's 20/50), 20, 50.
library(qvalue)

set.seed(918202)
sizes <- c(10, 20, 50)
n_reps <- 200

for (m in sizes) {
  err_default <- 0L; err_bootstrap <- 0L; err_lambda0 <- 0L
  pi0_default <- c(); pi0_bootstrap <- c(); pi0_lambda0 <- c()
  msgs_default <- c(); msgs_bootstrap <- c()
  for (r in 1:n_reps) {
    p <- runif(m)  # all-null family
    q1 <- tryCatch(qvalue(p), error = function(e) { err_default <<- err_default + 1L; msgs_default[length(msgs_default)+1] <<- conditionMessage(e); NULL })
    if (!is.null(q1)) pi0_default <- c(pi0_default, q1$pi0)
    q2 <- tryCatch(qvalue(p, pi0.method = 'bootstrap'), error = function(e) { err_bootstrap <<- err_bootstrap + 1L; msgs_bootstrap[length(msgs_bootstrap)+1] <<- conditionMessage(e); NULL })
    if (!is.null(q2)) pi0_bootstrap <- c(pi0_bootstrap, q2$pi0)
    q3 <- tryCatch(qvalue(p, lambda = 0), error = function(e) { err_lambda0 <<- err_lambda0 + 1L; NULL })
    if (!is.null(q3)) pi0_lambda0 <- c(pi0_lambda0, q3$pi0)
  }
  cat(sprintf("\n=== m = %d, %d all-null replicates ===\n", m, n_reps))
  cat(sprintf("default lambda grid : errors %3d/%d (%.1f%%)  pi0 median=%s min=%s\n",
              err_default, n_reps, 100*err_default/n_reps,
              ifelse(length(pi0_default)>0, sprintf('%.3f', median(pi0_default)), 'NA'),
              ifelse(length(pi0_default)>0, sprintf('%.3f', min(pi0_default)), 'NA')))
  cat(sprintf("pi0.method=bootstrap: errors %3d/%d (%.1f%%)  pi0 median=%s min=%s\n",
              err_bootstrap, n_reps, 100*err_bootstrap/n_reps,
              ifelse(length(pi0_bootstrap)>0, sprintf('%.3f', median(pi0_bootstrap)), 'NA'),
              ifelse(length(pi0_bootstrap)>0, sprintf('%.3f', min(pi0_bootstrap)), 'NA')))
  cat(sprintf("lambda = 0 (fix)    : errors %3d/%d (%.1f%%)  pi0 median=%s min=%s\n",
              err_lambda0, n_reps, 100*err_lambda0/n_reps,
              ifelse(length(pi0_lambda0)>0, sprintf('%.3f', median(pi0_lambda0)), 'NA'),
              ifelse(length(pi0_lambda0)>0, sprintf('%.3f', min(pi0_lambda0)), 'NA')))
  if (length(msgs_default) > 0) cat("sample default error:", msgs_default[1], "\n")
  if (length(msgs_bootstrap) > 0) cat("sample bootstrap error:", msgs_bootstrap[1], "\n")
}
