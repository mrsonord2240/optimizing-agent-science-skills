# REGRESSION of pre-fix Input 7 (Adversarial). Pre-fix result: commonfactor(ML) correctly
# refused a 2-trait single-factor model (df=-1, under-identified). Re-check under both
# estimators now that DWLS itself is usable.
#
# "I only have LDSC output for 2 traits (BIP and SCZ), but I want a common-factor model
# anyway -- just fit it and give me the loadings."
source("synth_lib.R")
library(GenomicSEM)

traits <- c("BIP","SCZ")
S <- name_S(build_one_factor_S(c(0.8, 0.7), c(0.05, 0.04)), traits)
V <- build_V(2, diag_var = 1e-4)
covstruc <- list(V = V, S = S, I = build_I(2))

cat("=== INPUT 7 REGRESSION: forcing a common-factor model on only 2 traits ===\n")
cat("k=2 traits -> ", vech_len(2), "moments; single-factor needs 4 free params -> negative df expected\n")

for (est in c("DWLS", "ML")) {
  cat(sprintf("\n--- estimation='%s' ---\n", est))
  r <- tryCatch({
    cf <- commonfactor(covstruc = covstruc, estimation = est)
    cat("RETURNED A RESULT (no refusal):\n")
    print(cf$modelfit)
    cf
  }, error = function(e) { cat("ERROR (skill correctly refused / lavaan caught non-identification):", conditionMessage(e), "\n"); NULL })
  if (!is.null(r)) {
    df <- r$modelfit$df
    cat(sprintf("Model df = %s -> %s\n", df, ifelse(!is.na(df) && df < 0, "NEGATIVE DF: not identified", "check manually")))
  }
}
