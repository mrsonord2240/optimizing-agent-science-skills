# INPUT 2 (Variant A): "Run a common-factor GWAS across MDD, anxiety, and PTSD using
# commonfactorGWAS with DWLS estimation. Report SNPs with factor p<5e-8 AND Q_SNP
# p > Bonferroni threshold. Exclude Q_SNP-significant SNPs from the common-factor list."
# (This is the Skill usage-guide.md's own suggested prompt, verbatim in spirit.)
#
# SYNTHETIC SNP panel: 20 SNPs. 5 are planted pure "factor SNPs" (same-direction effect
# proportional to loadings on all 3 traits, small |beta|). 5 are planted "heterogeneous"
# SNPs (large effect on ONE trait only, ~0 on the others) -- these should show up as
# factor-significant-but-Q_SNP-significant OR simply trait-specific. 10 are null.
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
se <- matrix(0.01, n, 3)  # fixed SE for simplicity

beta <- matrix(0, n, 3)
# Factor SNPs: true effect on the latent factor, propagated proportional to loadings
factor_true_effect <- 0.05
for (i in 1:n_factor) beta[i, ] <- factor_true_effect * loadings
# Heterogeneous SNPs: large effect on trait 1 (MDD) only -> violates common-factor assumption
for (i in (n_factor+1):(n_factor+n_het)) beta[i, ] <- c(0.15, 0.0, 0.0)
# Null SNPs: tiny noise only
for (i in (n_factor+n_het+1):n) beta[i, ] <- rnorm(3, 0, 0.002)

SNPs <- data.frame(
  SNP = paste0("rs", 1:n), A1 = "A", A2 = "G", MAF = maf,
  beta.MDD = beta[,1], se.MDD = se[,1],
  beta.ANX = beta[,2], se.ANX = se[,2],
  beta.PTSD = beta[,3], se.PTSD = se[,3]
)
cat("=== INPUT 2: commonfactorGWAS with Q_SNP classification ===\n")
cat("Planted: SNPs 1-5 = factor SNPs, 6-10 = heterogeneous (MDD-specific), 11-20 = null\n")

cat("\n--- Attempt with DWLS (Skill's default) ---\n")
r <- tryCatch(commonfactorGWAS(covstruc = covstruc, SNPs = SNPs, estimation = "DWLS",
                                parallel = FALSE, cores = 1),
              error = function(e) { cat("DWLS ERROR:", conditionMessage(e), "\n"); NULL })

cat("\n--- Attempt with ML ---\n")
r2 <- tryCatch(commonfactorGWAS(covstruc = covstruc, SNPs = SNPs, estimation = "ML",
                                 parallel = FALSE, cores = 1),
               error = function(e) { cat("ML ERROR:", conditionMessage(e), "\n"); NULL })

if (!is.null(r2)) {
  cat("\nSUCCESS. Output columns:", paste(colnames(r2), collapse=", "), "\n")
  print(r2)
} else {
  cat("\nRESULT: commonfactorGWAS is non-functional under BOTH estimators in this environment.\n")
}
