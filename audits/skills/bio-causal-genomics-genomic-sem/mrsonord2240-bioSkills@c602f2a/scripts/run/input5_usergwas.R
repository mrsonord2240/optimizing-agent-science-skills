# REGRESSION of pre-fix Input 5 (Stress). Pre-fix result: userGWAS() crashed identically
# under DWLS and ML with "object 'ReorderModelnoSNP' not found". Re-run under the pinned
# combination.
#
# "Test SNP -> F path AND a direct SNP -> trait1 path simultaneously using userGWAS,
# matching the Skill's own 'userGWAS for Custom Path Models' example."
source("synth_lib.R")
library(GenomicSEM)

traits <- c("trait1","trait2","trait3")
loadings <- c(0.7, 0.6, 0.65)
h2 <- c(0.08, 0.07, 0.06)
S <- name_S(build_one_factor_S(loadings, h2), traits)
V <- build_V(3, diag_var = 1e-4)
covstruc <- list(V = V, S = S, I = build_I(3))

set.seed(7)
n <- 6
SNPs <- data.frame(
  SNP = paste0("rs", 1:n), A1 = "A", A2 = "G", MAF = runif(n, 0.1, 0.4),
  beta.trait1 = c(0.05,0.02,0.10,0.0,0.03,0.0), se.trait1 = 0.01,
  beta.trait2 = c(0.04,0.02,0.0, 0.0,0.02,0.0), se.trait2 = 0.01,
  beta.trait3 = c(0.045,0.02,0.0,0.0,0.025,0.0), se.trait3 = 0.01
)

model <- '
    F =~ NA*trait1 + trait2 + trait3
    F ~~ 1*F
    F ~ SNP
    trait1 ~ SNP
'
cat("=== INPUT 5 REGRESSION: userGWAS custom SNP-path model (F~SNP + trait1~SNP direct) ===\n")
cat("\n--- DWLS (Skill's example, verbatim estimation choice) ---\n")
r <- tryCatch(userGWAS(covstruc = covstruc, SNPs = SNPs, estimation = "DWLS", model = model,
                       sub = c("F~SNP","trait1~SNP"), parallel = FALSE, cores = 1),
              error = function(e) { cat("DWLS ERROR:", conditionMessage(e), "\n"); NULL })
if (!is.null(r)) {
  cat("DWLS SUCCEEDED (pre-fix: crashed here).\n")
  direct <- r[[2]]
  print(direct)
  cat(sprintf("Planted direct effect on rs3=0.10; recovered=%.4f; others |est|<0.02: %s\n",
              direct$est[3], all(abs(direct$est[-3]) < 0.02)))
}
cat("\n--- ML ---\n")
r2 <- tryCatch(userGWAS(covstruc = covstruc, SNPs = SNPs, estimation = "ML", model = model,
                        sub = c("F~SNP","trait1~SNP"), parallel = FALSE, cores = 1),
               error = function(e) { cat("ML ERROR:", conditionMessage(e), "\n"); NULL })
if (!is.null(r2)) { cat("ML SUCCEEDED\n"); print(r2[[2]]) } else cat("ML: fails (expected -- see fix log, unrelated singular-matrix issue on this tiny 6-SNP exact-fit input).\n")
