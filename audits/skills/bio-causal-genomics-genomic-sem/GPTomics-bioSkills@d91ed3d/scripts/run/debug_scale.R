source("synth_lib.R")
library(GenomicSEM)
set.seed(1)
traits <- c("MDD", "ANX", "PTSD", "NEUR")
true_loadings <- c(0.75, 0.65, 0.70, 0.55)
h2 <- c(0.10, 0.06, 0.05, 0.12)
S <- name_S(build_one_factor_S(true_loadings, h2), traits)

for (dv in c(5e-4, 1e-4, 1e-5, 1e-3, 1e-2)) {
  V <- build_V(length(traits), diag_var = dv, overlap_frac = 0)
  covstruc <- list(V = V, S = S, I = build_I(length(traits)), N = c(150000,120000,90000,300000), m = 1173569)
  cat("\n\n===== diag_var =", dv, "=====\n")
  res <- tryCatch({
    cf <- commonfactor(covstruc = covstruc, estimation = "DWLS")
    cat("SUCCESS. CFI=", cf$modelfit$CFI, " RMSEA=", cf$modelfit$RMSEA, "\n")
    print(cf$results[cf$results$op=="=~", c("rhs","STD_Genotype")])
  }, error = function(e) cat("ERROR:", conditionMessage(e), "\n"))
}
