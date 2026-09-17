# Input 5 (Stress) -- Full sensitivity battery + bidirectional MR + Steiger + NOME check +
# SIMEX correction + STROBE-MR summary on a polygenic exposure with directional pleiotropy and
# a NOME (I^2_GX < 0.9) violation. SKILL.md's own text (Per-Method-Failure-Modes ->
# "IVW under directional pleiotropy" and "NOME violation invalidating Egger") describes the
# fix in PROSE ONLY -- it gives no inline SIMEX code block (unlike the sibling
# pleiotropy-detection Skill, which ships examples/simex_egger_correction.R). This tests
# whether an agent following just this Skill's prose reproduces a working SIMEX correction.

library(TwoSampleMR)
library(simex)

set.seed(55)
n_snps <- 40
# Weak-ish instruments (larger se relative to beta spread) to push I^2_GX below 0.9,
# plus a directional pleiotropic term (same-sign nuisance effect on outcome for all SNPs).
beta_exp <- rnorm(n_snps, 0.05, 0.015)
se_exp <- runif(n_snps, 0.02, 0.035)  # large relative to the spread of beta_exp -> low I^2_GX

true_beta_xy <- 0.4
directional_pleiotropy <- 0.02  # constant non-zero intercept term = directional pleiotropy
beta_out <- true_beta_xy * beta_exp + directional_pleiotropy + rnorm(n_snps, 0, 0.01)
se_out <- runif(n_snps, 0.015, 0.03)

dat <- data.frame(
  SNP = paste0('rs', 1:n_snps),
  beta.exposure = beta_exp, se.exposure = se_exp,
  beta.outcome = beta_out, se.outcome = se_out,
  effect_allele.exposure = 'A', other_allele.exposure = 'G',
  effect_allele.outcome = 'A', other_allele.outcome = 'G',
  eaf.exposure = runif(n_snps, 0.2, 0.8),
  exposure = 'Polygenic trait X', id.exposure = 'X', mr_keep.exposure = TRUE,
  outcome = 'Trait Y', id.outcome = 'Y', mr_keep.outcome = TRUE, mr_keep = TRUE,
  pval.exposure = 2 * pnorm(-abs(beta_exp / se_exp))
)

cat('--- Primary MR battery ---\n')
primary <- mr(dat, method_list = c('mr_ivw', 'mr_egger_regression', 'mr_weighted_median', 'mr_weighted_mode'))
print(primary[, c('method', 'nsnp', 'b', 'se', 'pval')])
cat('True causal beta_XY was:', true_beta_xy, '(directional pleiotropy intercept =', directional_pleiotropy, ')\n')

pleio <- mr_pleiotropy_test(dat)
cat('\n--- Egger intercept (directional pleiotropy test) ---\n')
cat('intercept:', signif(pleio$egger_intercept, 3), '| p:', signif(pleio$pval, 3), '\n')

isq <- TwoSampleMR::Isq(dat$beta.exposure, dat$se.exposure)
cat('\nI^2_GX:', round(isq, 3), if (isq < 0.9) '-- NOME VIOLATED; SIMEX correction required per SKILL.md' else '-- NOME OK', '\n')

if (isq < 0.9) {
  cat('\n--- Attempting SIMEX-corrected Egger, following SKILL.md prose\n')
  cat('    ("SIMEX-correct via the simex package applied to the Egger fit,\n')
  cat('     treating se.exposure as measurement error in beta.exposure") ---\n')
  attempt <- tryCatch({
    egger_lm <- lm(beta.outcome ~ beta.exposure, weights = 1 / dat$se.outcome^2, data = dat, x = TRUE, y = TRUE)
    simex_fit <- simex(egger_lm, SIMEXvariable = 'beta.exposure', measurement.error = dat$se.exposure,
                        fitting.method = 'quad', asymptotic = FALSE)
    summary(simex_fit)
  }, error = function(e) {
    cat('SIMEX ERROR:', conditionMessage(e), '\n')
    NULL
  })
  if (!is.null(attempt)) print(attempt)
}

cat('\n--- Bidirectional MR ---\n')
dat_rev <- data.frame(
  SNP = dat$SNP,
  beta.exposure = dat$beta.outcome, se.exposure = dat$se.outcome,
  beta.outcome = dat$beta.exposure, se.outcome = dat$se.exposure,
  effect_allele.exposure = dat$effect_allele.outcome, other_allele.exposure = dat$other_allele.outcome,
  effect_allele.outcome = dat$effect_allele.exposure, other_allele.outcome = dat$other_allele.exposure,
  eaf.exposure = dat$eaf.exposure,
  exposure = 'Trait Y', id.exposure = 'Y', mr_keep.exposure = TRUE,
  outcome = 'Polygenic trait X', id.outcome = 'X', mr_keep.outcome = TRUE, mr_keep = TRUE,
  pval.exposure = 2 * pnorm(-abs(dat$beta.outcome / dat$se.outcome))
)
rev_res <- mr(dat_rev, method_list = 'mr_ivw')
cat('Forward IVW: b=', signif(primary$b[primary$method == 'Inverse variance weighted'], 3),
    ' p=', signif(primary$pval[primary$method == 'Inverse variance weighted'], 3), '\n')
cat('Reverse IVW: b=', signif(rev_res$b, 3), ' p=', signif(rev_res$pval, 3), '\n')

steiger <- tryCatch(directionality_test(dat), error = function(e) { cat('STEIGER ERROR:', conditionMessage(e), '\n'); NULL })
if (!is.null(steiger) && nrow(steiger) > 0) {
  cat('Steiger correct direction:', steiger$correct_causal_direction, '| p:', signif(steiger$steiger_pval, 3), '\n')
} else {
  cat('Steiger: NOT PRODUCED (likely missing samplesize columns)\n')
}

cat('\n--- STROBE-MR summary ---\n')
cat('n SNPs:', n_snps, '| I^2_GX:', round(isq, 3), '| Egger intercept p:', signif(pleio$pval, 3), '\n')
cat('Primary IVW: b=', signif(primary$b[primary$method == 'Inverse variance weighted'], 3),
    ' p=', signif(primary$pval[primary$method == 'Inverse variance weighted'], 3), '\n')
