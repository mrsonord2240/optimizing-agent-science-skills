# INPUT 4 (Variant B): "Fit a two-factor confirmatory model: F1 = LDL+HDL+triglycerides,
# F2 = fasting glucose+HbA1c+2hr glucose, with F1~~F2 free to estimate factor correlation.
# Use usermodel with DWLS. Report fit indices and factor correlation." (This is the exact
# prompt template the Skill's own usage-guide.md suggests under "Confirmatory Two-Factor
# Model".) Ground truth: planted loadings per factor + planted factor correlation 0.40.
source("synth_lib.R")
library(GenomicSEM)

traits <- c("LDL","HDL","TG","FG","HbA1c","GLU2H")
load1 <- c(0.80, -0.60, 0.70)   # LDL, HDL, TG on F1 (lipid)
load2 <- c(0.65, 0.75, 0.60)    # FG, HbA1c, GLU2H on F2 (glycemic)
h2 <- c(0.12, 0.10, 0.09, 0.07, 0.06, 0.05)
rF <- 0.40  # planted factor correlation

Lambda <- matrix(0, 6, 2)
Lambda[1:3, 1] <- load1 * sqrt(h2[1:3])
Lambda[4:6, 2] <- load2 * sqrt(h2[4:6])
Psi <- matrix(c(1, rF, rF, 1), 2, 2)   # factor covariance (unit variances)
Theta <- diag(h2 - c(load1^2 * h2[1:3], load2^2 * h2[4:6]))
S <- Lambda %*% Psi %*% t(Lambda) + Theta
S <- name_S(S, traits)
V <- build_V(6, diag_var = 2e-4)

cat("=== INPUT 4: two-factor confirmatory usermodel (planted rF=0.40) ===\n")
check_pd(S, "S")

covstruc <- list(V = V, S = S, I = build_I(6))
model_syntax <- '
    F1 =~ NA*LDL + HDL + TG
    F2 =~ NA*FG + HbA1c + GLU2H
    F1 ~~ 1*F1
    F2 ~~ 1*F2
    F1 ~~ F2
'

cat("\n--- Attempt with DWLS (Skill's documented default) ---\n")
r <- tryCatch(usermodel(covstruc = covstruc, model = model_syntax, estimation = "DWLS"),
              error = function(e) { cat("DWLS ERROR:", conditionMessage(e), "\n"); NULL })

cat("\n--- Fallback: ML ---\n")
uf <- usermodel(covstruc = covstruc, model = model_syntax, estimation = "ML")
cat("\n--- Model fit ---\n"); print(uf$modelfit)
cat("\n--- Full results ---\n"); print(uf$results)

load_rows <- uf$results[uf$results$op == "=~", ]
cat("\nRecovered vs planted loadings:\n")
print(data.frame(trait = load_rows$rhs, recovered = round(load_rows$Standardized_Est,3),
                  planted = c(load1, load2)))

fcorr <- uf$results[uf$results$lhs == "F1" & uf$results$op == "~~" & uf$results$rhs == "F2", ]
cat(sprintf("\nRecovered factor correlation F1~~F2: %.4f (planted %.2f)\n",
            fcorr$Standardized_Est, rF))

cat("\nIdentification check: 3 indicators per factor (>=3 required per SKILL.md) -> ",
    ifelse(sum(load_rows$lhs=="F1")>=3 && sum(load_rows$lhs=="F2")>=3, "OK", "FAIL"), "\n")
