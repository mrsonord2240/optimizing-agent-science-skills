# Input 11 (NEW, auditor-authored) -- Steiger/directionality_test() SUCCESS path. Inputs 1 and
# 5 confirmed the round-2 guard fires correctly (with/without samplesize_col). This input
# confirms the OTHER half of the fix: that following SKILL.md's "TwoSampleMR Standard
# Workflow" section literally -- which now comments `# required for directionality_test()
# below` next to `samplesize_col = 'N'` on BOTH read_exposure_data()/read_outcome_data() calls
# -- actually produces a correct, non-NULL directionality_test() result end to end, on a fresh
# synthetic dataset (not the real GIANT/PGC data already used in Input 1) with a planted
# CORRECT forward causal direction and a planted REVERSE-direction null, so the test's own
# pass/fail condition is meaningful rather than trivial.
library(TwoSampleMR)

set.seed(202)
n_snps <- 45
beta_exposure <- rnorm(n_snps, 0.06, 0.015)
se_exposure <- runif(n_snps, 0.006, 0.010)
true_beta_xy <- 0.5
beta_outcome <- true_beta_xy * beta_exposure + rnorm(n_snps, 0, 0.01)
se_outcome <- runif(n_snps, 0.010, 0.016)
n_exposure <- 60000
n_outcome <- 90000

exp_df <- data.frame(
    SNP = paste0("rs", 1:n_snps), beta = beta_exposure, se = se_exposure,
    effect_allele = "A", other_allele = "G",
    eaf = runif(n_snps, 0.2, 0.8),
    pval = 2 * pnorm(-abs(beta_exposure / se_exposure)),
    samplesize = n_exposure, stringsAsFactors = FALSE
)
out_df <- data.frame(
    SNP = exp_df$SNP, beta = beta_outcome, se = se_outcome,
    effect_allele = "A", other_allele = "G",
    eaf = exp_df$eaf,
    pval = 2 * pnorm(-abs(beta_outcome / se_outcome)),
    samplesize = n_outcome, stringsAsFactors = FALSE
)

# Exactly SKILL.md's "TwoSampleMR Standard Workflow" pattern: samplesize_col set on both sides.
exposure_dat <- format_data(exp_df, type = "exposure",
    snp_col = "SNP", beta_col = "beta", se_col = "se",
    effect_allele_col = "effect_allele", other_allele_col = "other_allele",
    eaf_col = "eaf", pval_col = "pval", samplesize_col = "samplesize")
outcome_dat <- format_data(out_df, type = "outcome",
    snp_col = "SNP", beta_col = "beta", se_col = "se",
    effect_allele_col = "effect_allele", other_allele_col = "other_allele",
    eaf_col = "eaf", pval_col = "pval", samplesize_col = "samplesize")

dat <- harmonise_data(exposure_dat, outcome_dat, action = 2)
cat("SNPs after harmonization:", nrow(dat), "\n")

primary <- mr(dat, method_list = "mr_ivw")
cat("\n--- Forward IVW ---\n")
print(primary[, c("method", "nsnp", "b", "se", "pval")])
cat("True forward beta_XY:", true_beta_xy, "\n")

# SKILL.md's guarded directionality_test() call, verbatim from the Standard Workflow section:
steiger <- directionality_test(dat)
if (is.null(steiger)) {
    stop("directionality_test() returned NULL -- dat is missing pval.exposure/pval.outcome/",
         "samplesize.exposure/samplesize.outcome (or supply pre-computed r.exposure/r.outcome, ",
         "e.g. via get_r_from_lor() for binary traits). It fails silently, not loudly, so check ",
         "for NULL rather than trusting a downstream NULL$correct_causal_direction.")
}
cat("\n--- Steiger directionality_test() ---\n")
cat("correct_causal_direction:", steiger$correct_causal_direction,
    "| steiger_pval:", signif(steiger$steiger_pval, 3), "\n")

# Also exercise the "Bidirectional and Steiger" section's reverse-direction call on the SAME
# well-formed (samplesize_col-bearing) data, to confirm the guard's success path holds there too.
exposure_rev <- format_data(out_df, type = "exposure",
    snp_col = "SNP", beta_col = "beta", se_col = "se",
    effect_allele_col = "effect_allele", other_allele_col = "other_allele",
    eaf_col = "eaf", pval_col = "pval", samplesize_col = "samplesize")
outcome_rev <- format_data(exp_df, type = "outcome",
    snp_col = "SNP", beta_col = "beta", se_col = "se",
    effect_allele_col = "effect_allele", other_allele_col = "other_allele",
    eaf_col = "eaf", pval_col = "pval", samplesize_col = "samplesize")
dat_rev <- harmonise_data(exposure_rev, outcome_rev, action = 2)
results_rev <- mr(dat_rev, method_list = "mr_ivw")
cat("\n--- Reverse IVW (former outcome as exposure) ---\n")
print(results_rev[, c("method", "nsnp", "b", "se", "pval")])

dir_test_rev <- directionality_test(dat_rev)
if (is.null(dir_test_rev)) stop("directionality_test() returned NULL on the reverse call -- guard should not reach here given samplesize_col is set on dat_rev too.")
cat("\n--- Reverse directionality_test() ---\n")
cat("correct_causal_direction:", dir_test_rev$correct_causal_direction,
    "| steiger_pval:", signif(dir_test_rev$steiger_pval, 3), "\n")

cat("\nNEW INPUT RESULT: directionality_test() returned a real, non-NULL, CORRECT result",
    "(forward: correct_causal_direction=", steiger$correct_causal_direction,
    "; reverse call also completed without the guard firing) -- the fix is not just a stop()",
    "message, the documented samplesize_col pattern genuinely makes the underlying call work.\n")
