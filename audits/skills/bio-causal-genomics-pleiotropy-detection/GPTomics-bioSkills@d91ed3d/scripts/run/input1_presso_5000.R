# Companion to input1_canonical.R: MR-PRESSO on the same real BMI15 x MDD18 data at
# NbDistribution=5000 (still real, just below the SKILL's "stringent" 10000 tier) --
# run separately because NbDistribution=10000 on 95 real SNPs did not complete within
# a long wait on this shared audit machine (see eval_viewer notes on Input 1
# Efficiency). This confirms PRESSO itself executes correctly on the real dataset;
# only the specific 10000-distribution "stringent" configuration was too slow to
# observe in this session.

library(TwoSampleMR)
library(MRPRESSO)

bmi <- readRDS('F:/OpenScience/audit-envs/mendelian-randomization-analyst/public-data/MRMix_BMI15.rds')
mdd <- readRDS('F:/OpenScience/audit-envs/mendelian-randomization-analyst/public-data/MRMix_MDD18.rds')
exp_dat <- data.frame(SNP = bmi$SNP, beta.exposure = bmi$beta, se.exposure = bmi$se,
  effect_allele.exposure = bmi$effect_allele, other_allele.exposure = bmi$other_allele,
  eaf.exposure = bmi$EAF, pval.exposure = bmi$pval, exposure = 'BMI (GIANT 2015)',
  id.exposure = 'BMI15', mr_keep.exposure = TRUE)
out_dat <- data.frame(SNP = mdd$SNP, beta.outcome = log(mdd$OR), se.outcome = mdd$SE,
  effect_allele.outcome = mdd$A1, other_allele.outcome = mdd$A2,
  eaf.outcome = mdd$FRQ_A_59851, pval.outcome = mdd$P, outcome = 'MDD (PGC 2018)',
  id.outcome = 'MDD18', mr_keep.outcome = TRUE)
dat <- harmonise_data(exp_dat, out_dat)
dat <- dat[dat$mr_keep, ]

presso <- mr_presso(BetaOutcome='beta.outcome', BetaExposure='beta.exposure',
                     SdOutcome='se.outcome', SdExposure='se.exposure',
                     OUTLIERtest=TRUE, DISTORTIONtest=TRUE,
                     data=dat, NbDistribution=5000, SignifThreshold=0.05)
global_p <- presso$`MR-PRESSO results`$`Global Test`$Pvalue
main <- presso$`Main MR results`
n_outliers <- sum(presso$`MR-PRESSO results`$`Outlier Test`$Pvalue < 0.05, na.rm=TRUE)
cat('n SNPs:', nrow(dat), '\n')
cat('Global test p:', global_p, '\n')
cat('Outliers:', n_outliers, '/', nrow(dat), '\n')
cat('Raw IVW:', round(main$`Causal Estimate`[1], 4), '  Corrected:', round(main$`Causal Estimate`[2], 4), '\n')
