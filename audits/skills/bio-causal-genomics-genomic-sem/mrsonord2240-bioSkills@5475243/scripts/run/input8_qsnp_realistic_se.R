# NEW INPUT 8 (this audit; not in the pre-fix set). Targets the fix log's open question:
# under estimation='DWLS', commonfactorGWAS()'s Q_pval did not discriminate the planted
# heterogeneous SNPs from planted factor SNPs on the pre-fix/fixer's synthetic covstruc
# (flat SE=0.01 for every SNP regardless of MAF/N) -- while ML did, on the identical
# input. The fixer's hypothesis: this is an artifact of the synthetic panel lacking the
# real per-SNP N/MAF-driven sampling-variance structure a genuine sumstats()+ldsc()
# pipeline would supply, not a general DWLS-Q_SNP defect.
#
# This input tests that hypothesis directly: same planted classes (5 factor SNPs, 5
# heterogeneous SNPs, 10 null), but SE is now MAF- and N-driven exactly as a real GWAS
# would produce it: se_i = 1 / sqrt(2 * N * MAF_i * (1 - MAF_i)), N = 50000. This is the
# one deliberate design change from input2_cfgwas.R (which reused the pre-fix flat-SE
# panel as a same-conditions regression test).
#
# "Run a common-factor GWAS across MDD, anxiety, and PTSD with realistic per-SNP
# precision (SE varying by allele frequency, as ldsc()+sumstats() output would). Does
# DWLS estimation correctly flag the heterogeneous SNPs via Q_pval now?"
source("synth_lib.R")
library(GenomicSEM)

traits <- c("MDD","ANX","PTSD")
loadings <- c(0.75, 0.65, 0.70)
h2 <- c(0.10, 0.06, 0.05)
S <- name_S(build_one_factor_S(loadings, h2), traits)
V <- build_V(3, diag_var = 1e-4)
I <- build_I(3)
covstruc <- list(V = V, S = S, I = I)

set.seed(42)  # same seed/MAF draw as input2, for direct comparability
n_factor <- 5; n_het <- 5; n_null <- 10
n <- n_factor + n_het + n_null
maf <- runif(n, 0.05, 0.45)

N_gwas <- 50000
se_maf <- 1 / sqrt(2 * N_gwas * maf * (1 - maf))
cat("Per-SNP SE range (MAF/N-driven):", round(range(se_maf), 5), "\n")

beta <- matrix(0, n, 3)
factor_true_effect <- 0.05
for (i in 1:n_factor) beta[i, ] <- factor_true_effect * loadings
for (i in (n_factor+1):(n_factor+n_het)) beta[i, ] <- c(0.15, 0.0, 0.0)
for (i in (n_factor+n_het+1):n) beta[i, ] <- rnorm(3, 0, 0.002)

SNPs <- data.frame(
  SNP = paste0("rs", 1:n), A1 = "A", A2 = "G", MAF = maf,
  beta.MDD = beta[,1], se.MDD = se_maf,
  beta.ANX = beta[,2], se.ANX = se_maf,
  beta.PTSD = beta[,3], se.PTSD = se_maf
)
cat("=== INPUT 8: commonfactorGWAS Q_SNP discrimination with MAF/N-driven per-SNP SE ===\n")
cat("Planted: SNPs 1-5 = factor SNPs, 6-10 = heterogeneous (MDD-specific), 11-20 = null\n")

results <- list()
for (est in c("DWLS", "ML")) {
  cat(sprintf("\n--- estimation='%s' ---\n", est))
  r <- tryCatch(commonfactorGWAS(covstruc = covstruc, SNPs = SNPs, estimation = est,
                                  parallel = FALSE, cores = 1),
                error = function(e) { cat(est, "ERROR:", conditionMessage(e), "\n"); NULL })
  if (!is.null(r)) {
    results[[est]] <- r
    print(r[, c("SNP","MAF","est","Pval_Estimate","Q_pval")])
    het_flagged <- all(r$Q_pval[(n_factor+1):(n_factor+n_het)] < 1e-4)
    factor_clean <- all(r$Q_pval[1:n_factor] > 0.05)
    cat(sprintf("%s: heterogeneous SNPs Q_pval<1e-4 for all 5 = %s; factor SNPs Q_pval>0.05 for all 5 = %s\n",
                est, het_flagged, factor_clean))
    cat(sprintf("%s Q_pval range: het SNPs [%.4g, %.4g]; factor SNPs [%.4g, %.4g]\n",
                est, min(r$Q_pval[(n_factor+1):(n_factor+n_het)]), max(r$Q_pval[(n_factor+1):(n_factor+n_het)]),
                min(r$Q_pval[1:n_factor]), max(r$Q_pval[1:n_factor])))
  }
}

cat("\n=== CONCLUSION ===\n")
if (!is.null(results[["DWLS"]])) {
  het_ok <- all(results[["DWLS"]]$Q_pval[(n_factor+1):(n_factor+n_het)] < 1e-4)
  cat(ifelse(het_ok,
             "DWLS Q_pval NOW discriminates with MAF/N-driven SE -- supports the fixer's hypothesis that flat-SE was the artifact, not a general DWLS-Q_SNP defect.\n",
             "DWLS Q_pval STILL does not discriminate even with realistic per-SNP SE -- suggests the DWLS/Q_SNP weakness is not merely a flat-SE artifact and needs a real ldsc()-derived V to rule out further.\n"))
}
