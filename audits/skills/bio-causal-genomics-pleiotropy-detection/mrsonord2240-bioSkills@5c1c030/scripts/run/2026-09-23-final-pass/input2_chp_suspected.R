# Input 2 (Variant A, REGRESSION of pre-fix Input 2) -- "I suspect a shared heritable
# confounder between my exposure and outcome (LDSC rg would come out high). Run the
# standard UHP battery plus MR-PRESSO and tell me whether the result is trustworthy."
# Synthetic data (data/synth_chp.rds, reused byte-identical from the pre-fix audit) with
# PLANTED correlated horizontal pleiotropy: ground truth causal effect = 0, but a
# shared-confounder mechanism (alpha_j = 0.9*gamma_j + noise) manufactures an apparent
# positive association. Tests SKILL.md's "MR-PRESSO false negative under CHP" section,
# unchanged by the fix pass -- this is a regression check that the fix pass did not
# disturb this already-correct documented behavior.

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
set.seed(42)
presso <- mr_presso(BetaOutcome='beta.outcome', BetaExposure='beta.exposure',
                     SdOutcome='se.outcome', SdExposure='se.exposure',
                     OUTLIERtest=TRUE, DISTORTIONtest=TRUE,
                     data=dat, NbDistribution=2000, SignifThreshold=0.05)
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
  cat('CONFIRMED (regression holds): exactly the failure mode SKILL.md documents -- IVW is significantly biased by CHP,\n')
  cat('           and MR-PRESSO global test does NOT flag it. A CHP-aware method (CAUSE/LHC-MR) is required.\n')
} else {
  cat('Pattern not reproduced with this seed/effect size; see notes.\n')
}
