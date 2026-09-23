# REGRESSION of pre-fix Input 4 (Variant B). Pre-fix result: usermodel() crashed
# identically under DWLS and ML with "object 'ReorderModel' not found" -- confirmed via
# source inspection that usermodel()'s internal reorder step ignores `estimation`
# entirely. Re-run under the pinned combination.
#
# "Fit a two-factor confirmatory model: F1=LDL+HDL+triglycerides, F2=fasting
# glucose+HbA1c+2hr glucose, with F1~~F2 free. Use usermodel with DWLS. Report fit
# indices and factor correlation." Planted factor correlation rF=0.40.
source("synth_lib.R")
library(GenomicSEM)

traits <- c("LDL","HDL","TG","FG","HbA1c","GLU2H")
load1 <- c(0.80, -0.60, 0.70)
load2 <- c(0.65, 0.75, 0.60)
h2 <- c(0.12, 0.10, 0.09, 0.07, 0.06, 0.05)
rF <- 0.40

Lambda <- matrix(0, 6, 2)
Lambda[1:3, 1] <- load1 * sqrt(h2[1:3])
Lambda[4:6, 2] <- load2 * sqrt(h2[4:6])
Psi <- matrix(c(1, rF, rF, 1), 2, 2)
Theta <- diag(h2 - c(load1^2 * h2[1:3], load2^2 * h2[4:6]))
S <- Lambda %*% Psi %*% t(Lambda) + Theta
S <- name_S(S, traits)
V <- build_V(6, diag_var = 2e-4)

cat("=== INPUT 4 REGRESSION: two-factor confirmatory usermodel (planted rF=0.40) ===\n")
check_pd(S, "S")
covstruc <- list(V = V, S = S, I = build_I(6))
model_syntax <- '
    F1 =~ NA*LDL + HDL + TG
    F2 =~ NA*FG + HbA1c + GLU2H
    F1 ~~ 1*F1
    F2 ~~ 1*F2
    F1 ~~ F2
'

for (est in c("DWLS", "ML")) {
  cat(sprintf("\n--- estimation='%s' ---\n", est))
  uf <- tryCatch(usermodel(covstruc = covstruc, model = model_syntax, estimation = est),
                 error = function(e) { cat(est, "ERROR:", conditionMessage(e), "\n"); NULL })
  if (!is.null(uf)) {
    cat("SUCCEEDED (pre-fix: crashed under both estimators).\n")
    print(uf$modelfit)
    # NOTE: usermodel() names its standardized-loading column "STD_Genotype", not
    # "Standardized_Est" (that name is what commonfactor() uses) -- an undocumented
    # column-naming inconsistency across GenomicSEM functions; SKILL.md never warns
    # agents this differs by function. Handle both, as the fixer's own smoke test does.
    std_col <- if ("Standardized_Est" %in% names(uf$results)) "Standardized_Est" else "STD_Genotype"
    load_rows <- uf$results[uf$results$op == "=~", ]
    print(data.frame(trait = load_rows$rhs, recovered = round(as.numeric(load_rows[[std_col]]),3),
                      planted = c(load1, load2)))
    fcorr <- uf$results[uf$results$lhs == "F1" & uf$results$op == "~~" & uf$results$rhs == "F2", ]
    cat(sprintf("Recovered factor correlation F1~~F2 (%s): %.4f (planted %.2f)\n",
                est, as.numeric(fcorr[[std_col]]), rF))
  }
}
