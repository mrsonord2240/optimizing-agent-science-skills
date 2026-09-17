# Input 7 (Adversarial) -- Prompt claims "two independent GWAS files" for exposure and outcome,
# but both are drawn from UK Biobank (same underlying sample). SKILL.md's own "Operational rule"
# (One-Sample vs Two-Sample Bias Direction section): "Whenever both GWAS came from UK Biobank...
# treat the analysis as one-sample-equivalent... Treating it as 'two-sample because separate GWAS
# files' is a common error and produces overestimates." True causal effect is planted at ZERO;
# any positive IVW estimate here is bias, not signal -- letting us test empirically whether
# naive two-sample IVW is misled the way SKILL.md predicts and whether the documented remedy
# (MR-RAPS, F>=20 floor, jackknife SE) is actually reachable from the same data.
#
# PROMPT (given to the agent alongside these files):
# "I have BMI GWAS summary stats (biobank_bmi.tsv) and T2D GWAS summary stats (biobank_t2d.tsv),
#  both are UK Biobank exports I downloaded separately from the UKB return catalogue. Run a
#  standard two-sample MR of BMI on T2D."

library(TwoSampleMR)

set.seed(77)
n_snps <- 50
true_beta_xy <- 0  # PLANTED GROUND TRUTH: no true causal effect

# Shared per-SNP confounding term U_g: represents a heritable confounder (or sample-overlap-induced
# correlated estimation error) common to both GWAS because they are run on the SAME UKB individuals.
U_g <- rnorm(n_snps, 0, 0.03)

beta_exp <- rnorm(n_snps, 0.06, 0.015) + U_g
se_exp <- runif(n_snps, 0.008, 0.015)

# Outcome effect = true causal path (zero) + the SAME confounding term U_g (same-sample correlation)
# + independent noise. This is the mechanism SKILL.md names: "sample correlation between IV-X and
# IV-Y residuals" biasing toward the confounded observational estimate.
beta_out <- true_beta_xy * beta_exp + U_g * 1.1 + rnorm(n_snps, 0, 0.008)
se_out <- runif(n_snps, 0.01, 0.02)

dat <- data.frame(
  SNP = paste0('rs', 1:n_snps),
  beta.exposure = beta_exp, se.exposure = se_exp,
  beta.outcome = beta_out, se.outcome = se_out,
  effect_allele.exposure = 'A', other_allele.exposure = 'G',
  effect_allele.outcome = 'A', other_allele.outcome = 'G',
  eaf.exposure = runif(n_snps, 0.2, 0.8),
  exposure = 'BMI (claimed independent UKB export)', id.exposure = 'BMI',
  outcome = 'T2D (claimed independent UKB export)', id.outcome = 'T2D',
  mr_keep.exposure = TRUE, mr_keep.outcome = TRUE, mr_keep = TRUE,
  pval.exposure = 2 * pnorm(-abs(beta_exp / se_exp))
)
dat$f_stat <- (dat$beta.exposure / dat$se.exposure)^2
cat('Mean F-statistic:', round(mean(dat$f_stat), 1), '(one-sample floor per SKILL.md is F>=20, not the usual F>=10)\n')

cat('\n--- Naive "two-sample" IVW (what a user asking for "standard two-sample MR" would get) ---\n')
naive_ivw <- mr(dat, method_list = 'mr_ivw')
print(naive_ivw[, c('method', 'nsnp', 'b', 'se', 'pval')])
cat('TRUE causal beta_XY was:', true_beta_xy, '-- any nonzero estimate above is pure one-sample-equivalent bias\n')

cat('\n--- MR-RAPS (SKILL.md-recommended remedy once one-sample-equivalent is correctly diagnosed) ---\n')
raps <- tryCatch(
  TwoSampleMR::mr_raps(b_exp = dat$beta.exposure, b_out = dat$beta.outcome,
                        se_exp = dat$se.exposure, se_out = dat$se.outcome),
  error = function(e) { cat('MR-RAPS ERROR:', conditionMessage(e), '\n'); NULL }
)
if (!is.null(raps)) {
  cat('beta:', signif(raps$b, 3), '| se:', signif(raps$se, 3), '| p:', signif(raps$pval, 3), '\n')
}

cat('\n--- Verdict against ground truth ---\n')
cat('Naive IVW b =', signif(naive_ivw$b, 3), '(bias toward the confounded/observational direction,\n')
cat('  as SKILL.md predicts for one-sample F<10: "toward confounded observational estimate")\n')
if (!is.null(raps)) cat('MR-RAPS b =', signif(raps$b, 3), '-- does MR-RAPS alone fix a same-sample confounder? (see note)\n')
cat('NOTE: MR-RAPS is a weak-instrument correction, not a confounder-adjustment method; SKILL.md\n')
cat('  itself recommends it for the weak-IV component of one-sample bias, but the correct full\n')
cat('  remedy per SKILL.md is Burgess 2016 sample-overlap-corrected IVW (needs the cross-trait\n')
cat('  LDSC intercept) or moving the outcome to an external cohort (FinnGen/BBJ/MVP) --\n')
cat('  MR-RAPS on its own does not remove confounder-driven correlated-error bias.\n')
