# INPUT 3 (Edge): "Two of my four traits (BMI and WHR-adjBMI) are genetically almost
# identical (rg ~0.97). Fit a common-factor model across all four and diagnose any
# Heywood case." Ground truth: near-collinear pair should push one specific/residual
# variance toward/below 0 (Heywood case), exactly the failure mode the Skill documents
# under "Heywood case (negative residual variance)".
source("synth_lib.R")
library(GenomicSEM)

traits <- c("BMI", "WHRadjBMI", "T2D", "HDL")
# rg(BMI, WHRadjBMI) = 0.97 (near-collinear); other pairs modest.
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

cat("=== INPUT 3: Heywood-case diagnosis (near-collinear BMI / WHRadjBMI, rg=0.97) ===\n")
cat("Planted genetic correlation matrix:\n"); print(rg)
check_pd(S, "S")

covstruc <- list(V = V, S = S, I = build_I(4))
cf <- tryCatch(commonfactor(covstruc = covstruc, estimation = "ML"),
               error = function(e) { cat("ERROR:", conditionMessage(e), "\n"); NULL },
               warning = function(w) { cat("WARNING (caught):", conditionMessage(w), "\n");
                                        suppressWarnings(commonfactor(covstruc = covstruc, estimation = "ML")) })

if (!is.null(cf)) {
  cat("\n--- Model fit ---\n"); print(cf$modelfit)
  cat("\n--- Results ---\n"); print(cf$results)
  loadings <- cf$results[cf$results$op == "=~", ]
  resid <- cf$results[cf$results$op == "~~" & cf$results$lhs == cf$results$rhs, ]
  cat("\nHeywood check -- any standardized loading > 1?\n")
  print(loadings[abs(loadings$Standardized_Est) > 1, c("rhs","Standardized_Est")])
  cat("Heywood check -- any residual (Unstandardized_Estimate) < 0?\n")
  print(resid[resid$Unstandardized_Estimate < 0, c("lhs","Unstandardized_Estimate")])
  n_heywood <- sum(abs(loadings$Standardized_Est) > 1) + sum(resid$Unstandardized_Estimate < 0, na.rm = TRUE)
  cat(sprintf("\nHeywood cases detected: %d\n", n_heywood))
}

cat("\n--- Diagnostic per SKILL.md 'Heywood case' section: inspect S for rg near 1 ---\n")
off <- rg; diag(off) <- 0
cat("Max |pairwise rg| among inputs:", max(abs(off)), "-> ", ifelse(max(abs(off))>0.9, "FLAG: near-multicollinear pair present (BMI/WHRadjBMI)", "OK"), "\n")
