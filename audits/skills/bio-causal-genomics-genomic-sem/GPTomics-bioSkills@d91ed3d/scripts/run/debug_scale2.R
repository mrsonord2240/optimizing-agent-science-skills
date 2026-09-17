source("synth_lib.R")
library(GenomicSEM)
set.seed(2)

try_fit <- function(S, V, label) {
  covstruc <- list(V = V, S = S, I = build_I(ncol(S)))
  cat("\n===== ", label, " =====\n")
  tryCatch({
    cf <- commonfactor(covstruc = covstruc, estimation = "DWLS")
    cat("SUCCESS. CFI=", cf$modelfit$CFI, " RMSEA=", cf$modelfit$RMSEA, "\n")
    print(cf$results[cf$results$op == "=~", c("rhs", "STD_Genotype")])
  }, error = function(e) cat("ERROR:", conditionMessage(e), "\n"))
}

# Test A: k=3 exact single factor, no noise
traits3 <- c("T1","T2","T3")
S3 <- name_S(build_one_factor_S(c(0.7,0.6,0.65), c(0.1,0.08,0.09)), traits3)
V3 <- build_V(3, diag_var = 1e-4)
try_fit(S3, V3, "k=3 exact factor, no noise")

# Test B: k=3 with small random noise added to off-diagonals (imperfect fit)
S3n <- S3
noise <- matrix(rnorm(9, sd = 0.0005), 3, 3); noise[lower.tri(noise)] <- t(noise)[lower.tri(noise)]
diag(noise) <- 0
S3n <- S3n + noise
try_fit(S3n, V3, "k=3 factor + noise on off-diag")

# Test C: k=4 with noise
traits4 <- c("MDD","ANX","PTSD","NEUR")
S4 <- name_S(build_one_factor_S(c(0.75,0.65,0.70,0.55), c(0.10,0.06,0.05,0.12)), traits4)
noise4 <- matrix(rnorm(16, sd = 0.0008), 4, 4); noise4[lower.tri(noise4)] <- t(noise4)[lower.tri(noise4)]
diag(noise4) <- 0
S4n <- S4 + noise4
V4 <- build_V(4, diag_var = 1e-4)
try_fit(S4n, V4, "k=4 factor + noise")

# Test D: use usermodel() with explicit syntax on the exact (no-noise) k=4 case
model_syntax <- '
    F =~ NA*MDD + ANX + PTSD + NEUR
    F ~~ 1*F
'
cat("\n===== usermodel() on exact k=4 (no noise) =====\n")
covstruc4 <- list(V = build_V(4, diag_var=1e-4), S = S4, I = build_I(4))
tryCatch({
  uf <- usermodel(covstruc = covstruc4, model = model_syntax, estimation = "DWLS")
  cat("SUCCESS. CFI=", uf$modelfit$CFI, " RMSEA=", uf$modelfit$RMSEA, "\n")
  print(uf$results)
}, error = function(e) cat("ERROR:", conditionMessage(e), "\n"))
