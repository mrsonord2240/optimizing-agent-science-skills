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
dat <- harmonise_data(exp_dat, out_dat, action = 2)
dat <- dat[dat$mr_keep, ]
cat('SNPs after harmonisation:', nrow(dat), '\n')
primary <- mr(dat, method_list = c('mr_ivw', 'mr_egger_regression', 'mr_weighted_median', 'mr_weighted_mode'))
print(primary[, c('method', 'nsnp', 'b', 'se', 'pval')])
het <- mr_heterogeneity(dat)
print(het[, c('method', 'Q', 'Q_df', 'Q_pval')])
pleio <- mr_pleiotropy_test(dat)
cat('Egger intercept:', signif(pleio$egger_intercept,3), 'p:', signif(pleio$pval,3), '\n')
isq <- TwoSampleMR::Isq(dat$beta.exposure, dat$se.exposure)
cat('I^2_GX:', round(isq,3), '\n')
raps <- tryCatch(TwoSampleMR::mr_raps(dat$beta.exposure, dat$beta.outcome, dat$se.exposure, dat$se.outcome), error=function(e) {cat('RAPS ERR:', conditionMessage(e),'\n'); NULL})
if(!is.null(raps)) cat('RAPS b:', signif(raps$b,3), 'se:', signif(raps$se,3), 'p:', signif(raps$pval,3), '\n')
steiger <- tryCatch(directionality_test(dat), error=function(e){cat('STEIGER ERR:', conditionMessage(e),'\n'); NULL})
if(!is.null(steiger) && nrow(steiger)>0) { cat('Steiger correct dir:', steiger$correct_causal_direction, 'p:', signif(steiger$steiger_pval,3), '\n') } else cat('Steiger NOT PRODUCED\n')
loo <- mr_leaveoneout(dat)
cat('LOO range:', signif(min(loo$b),3), signif(max(loo$b),3), '\n')
cat('DONE_NO_PRESSO\n')
