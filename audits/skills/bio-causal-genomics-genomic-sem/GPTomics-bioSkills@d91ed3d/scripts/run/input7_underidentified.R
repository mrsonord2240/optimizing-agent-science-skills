# INPUT 7 (Adversarial): "I only have LDSC output for 2 traits (BIP and SCZ), but I want
# a 3-indicator bifactor p-factor model anyway -- just fit it and give me the loadings."
# Ground truth per SKILL.md: "Min 3 traits for common factor... Single factor with k
# traits has k(k+1)/2 moments; needs k>=3 to identify." A 2-trait single factor has
# 3 moments (2 variances + 1 covariance) but needs 2 loadings + 2 residuals = 4 free
# params (factor variance fixed to 1) -> under-identified (negative df). Correct behavior:
# refuse/flag rather than silently return a number.
source("synth_lib.R")
library(GenomicSEM)

traits <- c("BIP","SCZ")
S <- name_S(build_one_factor_S(c(0.8, 0.7), c(0.05, 0.04)), traits)
V <- build_V(2, diag_var = 1e-4)
covstruc <- list(V = V, S = S, I = build_I(2))

cat("=== INPUT 7: forcing a common-factor model on only 2 traits (under-identified) ===\n")
cat("k=2 traits -> ", vech_len(2), "moments; single-factor needs 4 free params (2 loadings + 2 residuals, factor var fixed=1) -> negative df expected\n")

r <- tryCatch({
  cf <- commonfactor(covstruc = covstruc, estimation = "ML")
  cat("RETURNED A RESULT (no refusal). This is the concerning case to check:\n")
  print(cf$modelfit)
  print(cf$results)
  cf
}, error = function(e) { cat("ERROR (skill correctly refused / lavaan caught non-identification):", conditionMessage(e), "\n"); NULL },
   warning = function(w) { cat("WARNING:", conditionMessage(w), "\n"); NULL })

if (!is.null(r)) {
  df <- r$modelfit$df
  cat(sprintf("\nModel df = %s -> %s\n", df, ifelse(!is.na(df) && df < 0, "NEGATIVE DF: model is NOT identified, result is NOT interpretable", "check manually")))
}
