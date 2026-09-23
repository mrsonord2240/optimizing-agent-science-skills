# Input 3 (regression) -- 3-SNP sparse cis-instrument set, below Egger's 10-SNP and
# MR-PRESSO's 4-SNP documented floors. Synthetic, planted true beta_XY = 0.35.
library(TwoSampleMR)
library(MRPRESSO)

set.seed(11)
n_snps <- 3
true_beta_xy <- 0.35

beta_exp <- c(0.09, 0.12, 0.07)
se_exp <- c(0.010, 0.012, 0.009)
beta_out <- beta_exp * true_beta_xy + rnorm(n_snps, 0, 0.004)
se_out <- c(0.015, 0.017, 0.014)

dat <- data.frame(
    SNP = paste0("rs", 1:n_snps),
    beta.exposure = beta_exp, se.exposure = se_exp,
    beta.outcome = beta_out, se.outcome = se_out,
    effect_allele.exposure = "A", other_allele.exposure = "G",
    effect_allele.outcome = "A", other_allele.outcome = "G",
    mr_keep = TRUE, id.exposure = "exp", id.outcome = "out",
    exposure = "exp", outcome = "out"
)

f_stat <- (dat$beta.exposure / dat$se.exposure)^2
cat("F-statistics:", round(f_stat, 1), "\n")

cat("--- IVW (3 SNPs) ---\n")
ivw <- mr(dat, method_list = "mr_ivw")
print(ivw[, c("method", "nsnp", "b", "se", "pval")])
cat("True causal beta_XY was:", true_beta_xy, "\n")

cat("\n--- Attempting Egger anyway (SKILL.md: needs >=10 SNPs for power) ---\n")
egger <- mr(dat, method_list = "mr_egger_regression")
print(egger[, c("method", "nsnp", "b", "se", "pval")])

cat("\n--- Attempting MR-PRESSO ---\n")
res <- tryCatch({
    mr_presso(BetaOutcome = "beta.outcome", BetaExposure = "beta.exposure",
              SdOutcome = "se.outcome", SdExposure = "se.exposure",
              OUTLIERtest = TRUE, DISTORTIONtest = TRUE,
              data = dat, NbDistribution = 1000, SignifThreshold = 0.05)
}, error = function(e) {
    cat("MR-PRESSO ERROR (expected per SKILL.md's Common Errors table):", conditionMessage(e), "\n")
    NULL
})
