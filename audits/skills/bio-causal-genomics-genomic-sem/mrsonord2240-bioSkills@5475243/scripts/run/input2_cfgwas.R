# REGRESSION of pre-fix Input 2 (Variant A). Pre-fix result: commonfactorGWAS() crashed
# under BOTH DWLS and ML with "object 'ReorderModel' not found" -- zero output, the
# Skill's flagship named capability. Re-run under the pinned combination.
#
# "Run a common-factor GWAS across MDD, anxiety, and PTSD using commonfactorGWAS with
# DWLS estimation. Report SNPs with factor p<5e-8 AND Q_SNP p > Bonferroni threshold."
# SYNTHETIC SNP panel: 20 SNPs. 5 planted pure "factor SNPs", 5 planted "heterogeneous"
# (large effect on MDD only), 10 null. Fixed SE=0.01 for all SNPs (flat-precision panel;
# see input8 for a MAF/N-driven-SE version of this same design).
source("synth_lib.R")
library(GenomicSEM)

traits <- c("MDD","ANX","PTSD")
loadings <- c(0.75, 0.65, 0.70)
h2 <- c(0.10, 0.06, 0.05)
S <- name_S(build_one_factor_S(loadings, h2), traits)
V <- build_V(3, diag_var = 1e-4)
I <- build_I(3)
covstruc <- list(V = V, S = S, I = I)

set.seed(42)
n_factor <- 5; n_het <- 5; n_null <- 10
n <- n_factor + n_het + n_null
maf <- runif(n, 0.05, 0.45)
se <- matrix(0.01, n, 3)

beta <- matrix(0, n, 3)
factor_true_effect <- 0.05
for (i in 1:n_factor) beta[i, ] <- factor_true_effect * loadings
for (i in (n_factor+1):(n_factor+n_het)) beta[i, ] <- c(0.15, 0.0, 0.0)
for (i in (n_factor+n_het+1):n) beta[i, ] <- rnorm(3, 0, 0.002)

SNPs <- data.frame(
  SNP = paste0("rs", 1:n), A1 = "A", A2 = "G", MAF = maf,
  beta.MDD = beta[,1], se.MDD = se[,1],
  beta.ANX = beta[,2], se.ANX = se[,2],
  beta.PTSD = beta[,3], se.PTSD = se[,3]
)
cat("=== INPUT 2 REGRESSION: commonfactorGWAS with Q_SNP classification ===\n")
cat("Planted: SNPs 1-5 = factor SNPs, 6-10 = heterogeneous (MDD-specific), 11-20 = null\n")

cat("\n--- DWLS (Skill's default) ---\n")
r <- tryCatch(commonfactorGWAS(covstruc = covstruc, SNPs = SNPs, estimation = "DWLS",
                                parallel = FALSE, cores = 1),
              error = function(e) { cat("DWLS ERROR:", conditionMessage(e), "\n"); NULL })
if (!is.null(r)) {
  cat("DWLS SUCCEEDED (pre-fix: crashed here).\n")
  print(r[, c("SNP","est","Pval_Estimate","Q_pval")])
  het_flagged <- all(r$Q_pval[(n_factor+1):(n_factor+n_het)] < 1e-4)
  factor_clean <- all(r$Q_pval[1:n_factor] > 0.05)
  cat(sprintf("DWLS Q_pval discriminates heterogeneous(<1e-4)=%s AND factor SNPs clean(>0.05)=%s\n",
              het_flagged, factor_clean))
  cat(sprintf("DWLS Q_pval range: het SNPs [%.4g, %.4g]; factor SNPs [%.4g, %.4g]\n",
              min(r$Q_pval[(n_factor+1):(n_factor+n_het)]), max(r$Q_pval[(n_factor+1):(n_factor+n_het)]),
              min(r$Q_pval[1:n_factor]), max(r$Q_pval[1:n_factor])))
}

cat("\n--- ML ---\n")
r2 <- tryCatch(commonfactorGWAS(covstruc = covstruc, SNPs = SNPs, estimation = "ML",
                                 parallel = FALSE, cores = 1),
               error = function(e) { cat("ML ERROR:", conditionMessage(e), "\n"); NULL })
if (!is.null(r2)) {
  cat("ML SUCCEEDED (pre-fix: crashed here too).\n")
  print(r2[, c("SNP","est","Pval_Estimate","Q_pval")])
  het_flagged2 <- all(r2$Q_pval[(n_factor+1):(n_factor+n_het)] < 1e-4)
  factor_clean2 <- all(r2$Q_pval[1:n_factor] > 0.05)
  cat(sprintf("ML Q_pval discriminates heterogeneous(<1e-4)=%s AND factor SNPs clean(>0.05)=%s\n",
              het_flagged2, factor_clean2))
} else {
  cat("\nRESULT: commonfactorGWAS still non-functional under ML -- REGRESSION.\n")
}
