# REGRESSION of pre-fix Input 3 (Edge). Pre-fix result: commonfactor(ML) correctly
# reproduced the Heywood case (BMI loading 1.061, residual -0.025). DWLS was not usable
# pre-fix; check both estimators now.
#
# "Two of my four traits (BMI and WHR-adjBMI) are genetically almost identical (rg~0.97).
# Fit a common-factor model across all four and diagnose any Heywood case."
source("synth_lib.R")
library(GenomicSEM)

traits <- c("BMI", "WHRadjBMI", "T2D", "HDL")
h2 <- c(0.20, 0.15, 0.08, 0.12)
rg <- matrix(c(
  1.00, 0.97, 0.35, -0.30,
  0.97, 1.00, 0.30, -0.25,
  0.35, 0.30, 1.00, -0.20,
  -0.30,-0.25,-0.20, 1.00
), 4, 4, byrow = TRUE)
S <- diag(sqrt(h2)) %*% rg %*% diag(sqrt(h2))
S <- name_S(S, traits)
V <- build_V(4, diag_var = 5e-4)

cat("=== INPUT 3 REGRESSION: Heywood-case diagnosis (near-collinear BMI/WHRadjBMI, rg=0.97) ===\n")
check_pd(S, "S")
covstruc <- list(V = V, S = S, I = build_I(4))

for (est in c("DWLS", "ML")) {
  cat(sprintf("\n--- estimation='%s' ---\n", est))
  cf <- tryCatch(commonfactor(covstruc = covstruc, estimation = est),
                 error = function(e) { cat(est, "ERROR:", conditionMessage(e), "\n"); NULL })
  if (!is.null(cf)) {
    cat("SUCCEEDED.\n")
    print(cf$modelfit)
    loadings <- cf$results[cf$results$op == "=~", ]
    resid <- cf$results[cf$results$op == "~~" & cf$results$lhs == cf$results$rhs, ]
    print(loadings[, c("rhs","Standardized_Est")])
    n_heywood <- sum(abs(loadings$Standardized_Est) > 1) + sum(resid$Unstandardized_Estimate < 0, na.rm = TRUE)
    cat(sprintf("Heywood cases detected (%s): %d\n", est, n_heywood))
  }
}
