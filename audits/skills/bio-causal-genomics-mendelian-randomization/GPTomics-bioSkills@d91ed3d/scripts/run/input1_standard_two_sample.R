# Input 1 (Canonical) -- Standard two-sample MR on real GIANT-BMI15 x PGC-MDD18 GWAS
# Following SKILL.md "TwoSampleMR Standard Workflow" pattern verbatim where columns allow.
# Data: F:/OpenScience/audit-envs/mendelian-randomization-analyst/public-data/{MRMix_BMI15,MRMix_MDD18}.rds
# Real, published GWAS (Locke 2015 Nature 518:197; Wray 2018 Nat Genet 50:668), NOT synthetic.

library(TwoSampleMR)

setwd('F:/OpenScience/audit-envs/mendelian-randomization-analyst')
bmi <- readRDS('public-data/MRMix_BMI15.rds')
mdd <- readRDS('public-data/MRMix_MDD18.rds')

exp_dat <- data.frame(
  SNP = bmi$SNP, beta.exposure = bmi$beta, se.exposure = bmi$se,
  effect_allele.exposure = bmi$effect_allele, other_allele.exposure = bmi$other_allele,
  eaf.exposure = bmi$EAF, pval.exposure = bmi$pval, samplesize.exposure = bmi$N,
  exposure = 'BMI (GIANT 2015)', id.exposure = 'BMI15', mr_keep.exposure = TRUE
)

out_dat <- data.frame(
  SNP = mdd$SNP, beta.outcome = log(mdd$OR), se.outcome = mdd$SE,
  effect_allele.outcome = mdd$A1, other_allele.outcome = mdd$A2,
  eaf.outcome = mdd$FRQ_A_59851, pval.outcome = mdd$P,
  samplesize.outcome = mdd$Nca + mdd$Nco,
  outcome = 'MDD (PGC 2018)', id.outcome = 'MDD18', mr_keep.outcome = TRUE
)

# F-statistic computed from EXPOSURE (Burgess 2011); SKILL.md's stated rule.
exp_dat$f_stat <- (exp_dat$beta.exposure / exp_dat$se.exposure)^2
cat('Mean F (all BMI15 top loci, pre-harmonisation):', round(mean(exp_dat$f_stat), 1), '\n')
cat('n SNPs with F < 10:', sum(exp_dat$f_stat < 10), '\n')

dat <- harmonise_data(exp_dat, out_dat, action = 2)
cat('\nSNPs after harmonisation:', sum(dat$mr_keep), '/', nrow(dat), '\n')
dat <- dat[dat$mr_keep, ]

primary <- mr(dat, method_list = c('mr_ivw', 'mr_egger_regression', 'mr_weighted_median', 'mr_weighted_mode'))
cat('\n--- Primary MR ---\n')
print(primary[, c('method', 'nsnp', 'b', 'se', 'pval')])

het <- mr_heterogeneity(dat)
cat('\n--- Heterogeneity (Cochran Q) ---\n')
print(het[, c('method', 'Q', 'Q_df', 'Q_pval')])

pleio <- mr_pleiotropy_test(dat)
cat('\n--- Egger intercept ---\n')
cat('intercept:', signif(pleio$egger_intercept, 3), '| se:', signif(pleio$se, 3), '| p:', signif(pleio$pval, 3), '\n')

isq <- TwoSampleMR::Isq(dat$beta.exposure, dat$se.exposure)
cat('\nI^2_GX:', round(isq, 3), if (isq < 0.9) ' -- NOME VIOLATED; SIMEX-correct Egger' else ' -- NOME OK', '\n')

raps <- tryCatch(
  TwoSampleMR::mr_raps(b_exp = dat$beta.exposure, b_out = dat$beta.outcome,
                        se_exp = dat$se.exposure, se_out = dat$se.outcome),
  error = function(e) { cat('MR-RAPS ERROR:', conditionMessage(e), '\n'); NULL }
)
if (!is.null(raps)) {
  cat('\n--- MR-RAPS ---\n')
  cat('beta:', signif(raps$b, 3), '| se:', signif(raps$se, 3), '| p:', signif(raps$pval, 3), '\n')
}

set.seed(1)
presso <- tryCatch(
  MRPRESSO::mr_presso(
    BetaOutcome = 'beta.outcome', BetaExposure = 'beta.exposure',
    SdOutcome = 'se.outcome', SdExposure = 'se.exposure',
    OUTLIERtest = TRUE, DISTORTIONtest = TRUE,
    data = dat, NbDistribution = 5000, SignifThreshold = 0.05
  ),
  error = function(e) { cat('MR-PRESSO ERROR:', conditionMessage(e), '\n'); NULL }
)
if (!is.null(presso)) {
  cat('\n--- MR-PRESSO ---\n')
  cat('Global RSSobs:', signif(presso$`MR-PRESSO results`$`Global Test`$RSSobs, 3),
      '| p:', signif(presso$`MR-PRESSO results`$`Global Test`$Pvalue, 3), '\n')
}

steiger <- tryCatch(directionality_test(dat), error = function(e) { cat('STEIGER ERROR:', conditionMessage(e), '\n'); NULL })
if (!is.null(steiger) && nrow(steiger) > 0) {
  cat('\n--- Steiger ---\n')
  cat('correct direction:', steiger$correct_causal_direction, '| p:', signif(steiger$steiger_pval, 3), '\n')
} else {
  cat('\n--- Steiger: NOT PRODUCED ---\n')
}

loo <- mr_leaveoneout(dat)
cat('\n--- Leave-one-out range of IVW estimate ---\n')
cat('min:', signif(min(loo$b), 3), '| max:', signif(max(loo$b), 3), '\n')

cat('\n--- STROBE-MR summary ---\n')
cat('Exposure SNPs harmonised:', nrow(dat), '| Mean F (post-harmonisation):', round(mean((dat$beta.exposure/dat$se.exposure)^2), 1), '\n')
cat('Primary IVW beta:', signif(primary$b[primary$method == 'Inverse variance weighted'], 3),
    '| p:', signif(primary$pval[primary$method == 'Inverse variance weighted'], 3), '\n')
