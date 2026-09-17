# INPUT 1 (Canonical): "I have LDSC output (S, V) for 4 correlated psychiatric GWAS
# (MDD, anxiety, PTSD, neuroticism). Fit a common-factor model with GenomicSEM, report
# CFI/RMSEA/SRMR and standardized loadings, and tell me if the model fits well."
#
# SYNTHETIC planted structure: single factor with true standardized loadings
# c(0.75, 0.65, 0.70, 0.55) on 4 traits with heritabilities h2 = c(0.10,0.06,0.05,0.12).
# S is constructed to be EXACTLY consistent with this one-factor structure so the fit
# should recover the planted loadings and show CFI=1 (a null/perfect-fit sanity check,
# not the ordinary case where a real S has estimation noise -- that noise lives in V here).
source("synth_lib.R")
library(GenomicSEM)

traits <- c("MDD", "ANX", "PTSD", "NEUR")
true_loadings <- c(0.75, 0.65, 0.70, 0.55)
h2 <- c(0.10, 0.06, 0.05, 0.12)

S <- name_S(build_one_factor_S(true_loadings, h2), traits)
V <- build_V(length(traits), diag_var = 1e-4, overlap_frac = 0)
I <- build_I(length(traits))

cat("=== INPUT 1: canonical common-factor CFA (SKILL's documented default: estimation='DWLS') ===\n")
covstruc <- list(V = V, S = S, I = I, N = c(150000,120000,90000,300000), m = 1173569)

cat("\n--- Attempt 1: estimation='DWLS' (the Skill's stated default, 'required when V is large') ---\n")
r_dwls <- tryCatch({
  commonfactor(covstruc = covstruc, estimation = "DWLS")
}, error = function(e) { cat("commonfactor(DWLS) ERROR:", conditionMessage(e), "\n"); NULL },
   warning = function(w) { cat("commonfactor(DWLS) WARNING:", conditionMessage(w), "\n"); NULL })
if (is.null(r_dwls)) cat("RESULT: DWLS path did not return a usable fit object (see FINDING in report).\n")

cat("\n--- Attempt 2: estimation='ML' (fallback) ---\n")
cf <- commonfactor(covstruc = covstruc, estimation = "ML")
cat("SUCCESS with ML.\n")
print(cf$modelfit)
print(cf$results)

cfi <- cf$modelfit$CFI
cat(sprintf("\nCFI=%s -> %s\n", cfi, ifelse(is.na(cfi), "NA", ifelse(cfi >= 0.95, "GOOD FIT", "check RMSEA/SRMR"))))

fit_rows <- cf$results[cf$results$op == "=~", ]
cat("\nRecovered standardized loadings vs planted:\n")
print(data.frame(trait = fit_rows$rhs, recovered = fit_rows$Standardized_Est, planted = true_loadings))
max_err <- max(abs(fit_rows$Standardized_Est - true_loadings))
cat(sprintf("Max abs error vs planted loadings: %.5f (ML estimator, exact-fit synthetic S)\n", max_err))
