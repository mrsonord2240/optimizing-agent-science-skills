source("synth_lib.R")
library(GenomicSEM)
library(lavaan)

traits <- c("MDD","ANX","PTSD","NEUR")
S <- name_S(build_one_factor_S(c(0.75,0.65,0.70,0.55), c(0.10,0.06,0.05,0.12)), traits)
V <- build_V(4, diag_var = 1e-4)
k <- 4
z <- k*(k+1)/2

Model1 <- "F1 =~ NA*MDD + ANX + PTSD + NEUR \n F1 ~~ 1*F1 \n"

W_Reorder <- diag(z)
diag(W_Reorder) <- diag(V)
W_Reorder <- solve(W_Reorder)

cat("Attempting direct lavaan::sem() call exactly as GenomicSEM does...\n")
fit <- tryCatch(
  sem(Model1, sample.cov = S, estimator = "DWLS", se = "standard",
      WLS.V = W_Reorder, sample.nobs = 2, optim.dx.tol = 0.01),
  warning = function(w) { cat("WARNING CAUGHT:", conditionMessage(w), "\n"); NULL },
  error = function(e) { cat("ERROR CAUGHT:", conditionMessage(e), "\n"); NULL }
)
if (!is.null(fit)) {
  cat("Converged:", lavInspect(fit, "converged"), "\n")
  print(summary(fit, fit.measures = TRUE, standardized = TRUE))
}

cat("\n\n--- Now with optim.force.converged / more iterations, no WLS.V restriction ---\n")
fit2 <- tryCatch(
  sem(Model1, sample.cov = S, estimator = "DWLS", se = "standard", sample.nobs = 2),
  warning = function(w) { cat("WARNING:", conditionMessage(w), "\n"); NULL },
  error = function(e) { cat("ERROR:", conditionMessage(e), "\n"); NULL }
)
if (!is.null(fit2)) cat("Converged (no WLS.V):", lavInspect(fit2, "converged"), "\n")
