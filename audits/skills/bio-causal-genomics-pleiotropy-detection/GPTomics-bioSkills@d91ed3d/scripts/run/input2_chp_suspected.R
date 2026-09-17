# Input 2 (Variant A) -- "I suspect a shared heritable confounder between my exposure
# and outcome (LDSC rg would come out high). Run the standard UHP battery plus
# MR-PRESSO and tell me whether the result is trustworthy." Synthetic data
# (data/synth_chp.rds) with PLANTED correlated horizontal pleiotropy: ground truth
# causal effect = 0, but a shared-confounder mechanism (alpha_j = 0.9*gamma_j + noise)
# manufactures an apparent positive association. This directly tests SKILL.md's claim
# under "MR-PRESSO false negative under CHP": "PRESSO global p > 0.05 (no detected
# pleiotropy) while a CHP-aware method... returns a substantially different (often
# null) causal estimate" and "MR-PRESSO's RSS-out distance is invariant under such a
# mean shift, so the global test is not powered against CHP."
# CAUSE itself is NOT installed in this environment (Stan/loo dependency chain,
# explicitly out of scope per the tooling brief) -- its code path is scored by
# inspection separately, not executed here.

library(TwoSampleMR)
library(MRPRESSO)

dat <- readRDS('F:/OpenScience/audits/bio-causal-genomics-pleiotropy-detection/data/synth_chp.rds')
cat('n SNPs:', nrow(dat), ' TRUE causal effect (ground truth): 0\n\n')

cat('=== IVW / Egger / median / mode ===\n')
res_mr <- mr(dat, method_list = c('mr_ivw', 'mr_egger_regression', 'mr_weighted_median', 'mr_weighted_mode'))
print(res_mr[, c('method', 'nsnp', 'b', 'se', 'pval')])

cat('\n=== Egger intercept ===\n')
pleio <- mr_pleiotropy_test(dat)
print(pleio)

cat('\n=== MR-PRESSO (global test for pleiotropy) ===\n')
presso <- mr_presso(BetaOutcome='beta.outcome', BetaExposure='beta.exposure',
                     SdOutcome='se.outcome', SdExposure='se.exposure',
                     OUTLIERtest=TRUE, DISTORTIONtest=TRUE,
                     data=dat, NbDistribution=5000, SignifThreshold=0.05)
global_p <- presso$`MR-PRESSO results`$`Global Test`$Pvalue
n_outliers <- sum(presso$`MR-PRESSO results`$`Outlier Test`$Pvalue < 0.05, na.rm=TRUE)
cat('Global test p:', global_p, '\n')
cat('Outliers flagged:', n_outliers, '/', nrow(dat), '\n')
main <- presso$`Main MR results`
cat('Raw IVW:', round(main$`Causal Estimate`[1], 4), '  Corrected IVW:', round(main$`Causal Estimate`[2], 4), '\n')

cat('\n=== Verdict ===\n')
ivw_p <- res_mr$pval[res_mr$method == 'Inverse variance weighted']
cat('IVW p:', format.pval(ivw_p), ' (ground truth is NULL; a significant result here is the CHP bias SKILL.md warns about)\n')
cat('PRESSO global p:', global_p, '(SKILL.md predicts this stays non-significant despite the bias -- CHP is not an outlier pattern)\n')
if (ivw_p < 0.05 && global_p > 0.05) {
  cat('CONFIRMED: exactly the failure mode SKILL.md documents -- IVW is significantly biased by CHP,\n')
  cat('           and MR-PRESSO global test does NOT flag it. A CHP-aware method (CAUSE/LHC-MR) is required.\n')
} else {
  cat('Pattern not reproduced with this seed/effect size; see notes.\n')
}
