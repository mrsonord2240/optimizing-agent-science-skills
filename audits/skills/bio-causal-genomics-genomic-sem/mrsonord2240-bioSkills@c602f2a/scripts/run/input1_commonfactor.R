# REGRESSION of pre-fix Input 1 (Canonical). Pre-fix result: commonfactor(DWLS) crashed
# with "object 'Model1_Results' not found"; ML fallback recovered planted loadings exactly.
# Re-run here under the fix's pinned combination (GenomicSEM 0.0.5 + lavaan 0.6.19, via
# r_gsem.sh) to confirm DWLS itself now works -- not just the ML fallback.
#
# "I have LDSC output (S, V) for 4 correlated psychiatric GWAS (MDD, anxiety, PTSD,
# neuroticism). Fit a common-factor model with GenomicSEM, report CFI/RMSEA/SRMR and
# standardized loadings, and tell me if the model fits well."
# SYNTHETIC planted structure: single factor with true standardized loadings
# c(0.75, 0.65, 0.70, 0.55) on 4 traits with heritabilities h2 = c(0.10,0.06,0.05,0.12).
source("synth_lib.R")
library(GenomicSEM)
cat(sprintf("GenomicSEM %s / lavaan %s\n", packageVersion("GenomicSEM"), packageVersion("lavaan")))

traits <- c("MDD", "ANX", "PTSD", "NEUR")
true_loadings <- c(0.75, 0.65, 0.70, 0.55)
h2 <- c(0.10, 0.06, 0.05, 0.12)

S <- name_S(build_one_factor_S(true_loadings, h2), traits)
V <- build_V(length(traits), diag_var = 1e-4, overlap_frac = 0)
I <- build_I(length(traits))

cat("=== INPUT 1 REGRESSION: canonical common-factor CFA ===\n")
covstruc <- list(V = V, S = S, I = I, N = c(150000,120000,90000,300000), m = 1173569)

cat("\n--- estimation='DWLS' (the Skill's stated default) ---\n")
r_dwls <- tryCatch({
  commonfactor(covstruc = covstruc, estimation = "DWLS")
}, error = function(e) { cat("commonfactor(DWLS) ERROR:", conditionMessage(e), "\n"); NULL })

if (!is.null(r_dwls)) {
  cat("DWLS SUCCEEDED (pre-fix: crashed here).\n")
  print(r_dwls$modelfit)
  fit_rows <- r_dwls$results[r_dwls$results$op == "=~", ]
  print(data.frame(trait = fit_rows$rhs, recovered = fit_rows$Standardized_Est, planted = true_loadings))
  max_err_dwls <- max(abs(fit_rows$Standardized_Est - true_loadings))
  cat(sprintf("DWLS max abs error vs planted loadings: %.5f\n", max_err_dwls))
} else {
  cat("DWLS still fails under the pinned combination -- REGRESSION.\n")
}

cat("\n--- estimation='ML' ---\n")
cf <- commonfactor(covstruc = covstruc, estimation = "ML")
cat("SUCCESS with ML.\n")
print(cf$modelfit)
print(cf$results)

cfi <- cf$modelfit$CFI
cat(sprintf("\nCFI=%s -> %s\n", cfi, ifelse(is.na(cfi), "NA", ifelse(cfi >= 0.95, "GOOD FIT", "check RMSEA/SRMR"))))

fit_rows <- cf$results[cf$results$op == "=~", ]
cat("\nRecovered standardized loadings vs planted (ML):\n")
print(data.frame(trait = fit_rows$rhs, recovered = fit_rows$Standardized_Est, planted = true_loadings))
max_err <- max(abs(fit_rows$Standardized_Est - true_loadings))
cat(sprintf("Max abs error vs planted loadings (ML): %.5f\n", max_err))
