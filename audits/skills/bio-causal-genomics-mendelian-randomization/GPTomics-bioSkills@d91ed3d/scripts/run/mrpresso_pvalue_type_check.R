library(TwoSampleMR)
setwd('F:/OpenScience/audit-envs/mendelian-randomization-analyst')
bmi <- readRDS('public-data/MRMix_BMI15.rds')
mdd <- readRDS('public-data/MRMix_MDD18.rds')
exp_dat <- data.frame(
  SNP = bmi$SNP, beta.exposure = bmi$beta, se.exposure = bmi$se,
  effect_allele.exposure = bmi$effect_allele, other_allele.exposure = bmi$other_allele,
  eaf.exposure = bmi$EAF, pval.exposure = bmi$pval,
  exposure = 'BMI', id.exposure = 'BMI15', mr_keep.exposure = TRUE)
out_dat <- data.frame(
  SNP = mdd$SNP, beta.outcome = log(mdd$OR), se.outcome = mdd$SE,
  effect_allele.outcome = mdd$A1, other_allele.outcome = mdd$A2,
  eaf.outcome = mdd$FRQ_A_59851, pval.outcome = mdd$P,
  outcome = 'MDD', id.outcome = 'MDD18', mr_keep.outcome = TRUE)
dat <- harmonise_data(exp_dat, out_dat, action = 2)
dat <- dat[dat$mr_keep, ]
presso <- MRPRESSO::mr_presso(BetaOutcome='beta.outcome', BetaExposure='beta.exposure',
  SdOutcome='se.outcome', SdExposure='se.exposure', OUTLIERtest=TRUE, DISTORTIONtest=TRUE,
  data=dat, NbDistribution=1000, SignifThreshold=0.05)
gt <- presso$`MR-PRESSO results`$`Global Test`
cat('class of Pvalue field:', class(gt$Pvalue), '\n')
cat('value:', gt$Pvalue, '\n')
print(gt)
cat('CHECK_DONE\n')
