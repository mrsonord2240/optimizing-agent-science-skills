source("synth_lib.R")
library(GenomicSEM)
traits <- c("MDD","ANX","PTSD","NEUR")
S <- name_S(build_one_factor_S(c(0.75,0.65,0.70,0.55), c(0.10,0.06,0.05,0.12)), traits)
V <- build_V(4, diag_var = 1e-4)
covstruc <- list(V=V, S=S, I=build_I(4))

cat("=== commonfactor with estimation='ML' ===\n")
res <- tryCatch({
  cf <- commonfactor(covstruc = covstruc, estimation = "ML")
  cat("SUCCESS. CFI=", cf$modelfit$CFI, " RMSEA=", cf$modelfit$RMSEA, "\n")
  print(cf$results)
}, error = function(e) cat("ERROR:", conditionMessage(e), "\n"))

cat("\n=== Direct lavaan::sem with ordered=FALSE fix, DWLS ===\n")
library(lavaan)
Model1 <- "F1 =~ NA*MDD + ANX + PTSD + NEUR \n F1 ~~ 1*F1 \n"
z <- 10
W_Reorder <- diag(z); diag(W_Reorder) <- diag(V); W_Reorder <- solve(W_Reorder)
fit <- tryCatch(
  sem(Model1, sample.cov = S, estimator = "DWLS", se = "standard",
      WLS.V = W_Reorder, sample.nobs = 2, optim.dx.tol = 0.01, ordered = FALSE),
  warning = function(w) { cat("WARNING:", conditionMessage(w), "\n"); NULL },
  error = function(e) { cat("ERROR:", conditionMessage(e), "\n"); NULL }
)
if (!is.null(fit)) {
  cat("Converged:", lavInspect(fit, "converged"), "\n")
  cat("CFI:", fitMeasures(fit, "cfi"), " RMSEA:", fitMeasures(fit, "rmsea"), "\n")
  print(standardizedSolution(fit))
}
