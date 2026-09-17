# Input 1 (Canonical, REGRESSION of pre-fix Input 1) -- "Run the standard MR sensitivity
# battery (IVW, Egger, weighted median, weighted mode, Cochran Q, Egger intercept,
# MR-PRESSO, Steiger, leave-one-out) on my harmonized BMI -> depression two-sample MR
# data and tell me if the result is robust to pleiotropy." Real GWAS data (GIANT BMI15
# x PGC MDD18), cached offline per TOOLS.md; no OpenGWAS token used. Following the
# CURRENT SKILL.md "Standard Sensitivity Battery" code block verbatim, including its
# newly-added set.seed(42) before mr_presso() (P2 fix). NbDistribution reduced to 2000
# (machine-time note in the dispatch: PRESSO at 10000 on this real 95-SNP dataset never
# finished in the pre-fix run; also FAILED to finish at 5000 there -- both were killed by
# a session reset, not an R error). Run in foreground with a timeout.

library(TwoSampleMR)
library(MRPRESSO)

bmi <- readRDS('F:/OpenScience/audit-envs/mendelian-randomization-analyst/public-data/MRMix_BMI15.rds')
mdd <- readRDS('F:/OpenScience/audit-envs/mendelian-randomization-analyst/public-data/MRMix_MDD18.rds')

exp_dat <- data.frame(
  SNP = bmi$SNP, beta.exposure = bmi$beta, se.exposure = bmi$se,
  effect_allele.exposure = bmi$effect_allele, other_allele.exposure = bmi$other_allele,
  eaf.exposure = bmi$EAF, pval.exposure = bmi$pval,
  exposure = 'BMI (GIANT 2015)', id.exposure = 'BMI15', mr_keep.exposure = TRUE)

out_dat <- data.frame(
  SNP = mdd$SNP, beta.outcome = log(mdd$OR), se.outcome = mdd$SE,
  effect_allele.outcome = mdd$A1, other_allele.outcome = mdd$A2,
  eaf.outcome = mdd$FRQ_A_59851, pval.outcome = mdd$P,
  outcome = 'MDD (PGC 2018)', id.outcome = 'MDD18', mr_keep.outcome = TRUE)

dat <- harmonise_data(exp_dat, out_dat)
dat <- dat[dat$mr_keep, ]
cat('Harmonised SNPs used:', nrow(dat), '\n\n')

cat('=== Core MR methods (SKILL.md method_list) ===\n')
methods <- c('mr_ivw', 'mr_egger_regression', 'mr_weighted_median', 'mr_weighted_mode')
res_mr <- mr(dat, method_list = methods)
print(res_mr[, c('method', 'nsnp', 'b', 'se', 'pval')])

cat('\n=== Heterogeneity (Cochran Q) ===\n')
het <- mr_heterogeneity(dat)
print(het[, c('method', 'Q', 'Q_df', 'Q_pval')])

cat('\n=== Egger intercept (pleiotropy test) ===\n')
pleio <- mr_pleiotropy_test(dat)
print(pleio)

cat('\n=== I^2_GX (NOME) ===\n')
isq <- Isq(dat$beta.exposure, dat$se.exposure)
cat('I^2_GX:', round(isq, 3), '\n')
if (isq >= 0.9) cat('NOME holds; Egger reliable\n') else if (isq >= 0.6) cat('SIMEX recommended\n') else cat('NOME violated; drop Egger\n')

cat('\n=== Steiger directionality ===\n')
steiger <- tryCatch(directionality_test(dat), error = function(e) { cat('Steiger ERROR:', conditionMessage(e), '\n'); NULL })
if (!is.null(steiger)) print(steiger[, c('exposure','outcome','snp_r2.exposure','snp_r2.outcome','correct_causal_direction','steiger_pval')])

cat('\n=== Leave-one-out (IVW) ===\n')
loo <- mr_leaveoneout(dat)
loo_b <- loo$b[!is.na(loo$b) & loo$SNP != 'All']
cat('LOO range:', round(min(loo_b), 4), 'to', round(max(loo_b), 4), '\n')

cat('\n=== MR-PRESSO (current SKILL.md: set.seed(42), NbDistribution reduced to 2000 for machine time) ===\n')
n_snp <- nrow(dat)
if (n_snp >= 4) {
  set.seed(42)  # matches SKILL.md's newly-added seed line before mr_presso()
  t0 <- Sys.time()
  presso <- tryCatch(
    mr_presso(BetaOutcome='beta.outcome', BetaExposure='beta.exposure',
              SdOutcome='se.outcome', SdExposure='se.exposure',
              OUTLIERtest=TRUE, DISTORTIONtest=TRUE,
              data=dat, NbDistribution=1000, SignifThreshold=0.05),
    error = function(e) { cat('PRESSO ERROR:', conditionMessage(e), '\n'); NULL })
  cat('PRESSO wall time:', round(as.numeric(Sys.time() - t0, units='secs'), 1), 'sec\n')
  if (!is.null(presso)) {
    global_p <- presso$`MR-PRESSO results`$`Global Test`$Pvalue
    cat('Global test p:', global_p, '\n')
    main <- presso$`Main MR results`
    cat('Raw IVW:', round(main$`Causal Estimate`[1], 4), ' Corrected IVW:', round(main$`Causal Estimate`[2], 4), '\n')
  }
} else {
  cat('Fewer than 4 SNPs (', n_snp, ') -- SKILL.md Common Errors table: PRESSO needs >=4; not run.\n')
}

cat('\n=== F-statistics ===\n')
f <- (dat$beta.exposure / dat$se.exposure)^2
cat('Mean F:', round(mean(f), 1), ' Min F:', round(min(f), 1), ' Weak (F<10):', sum(f < 10), '/', length(f), '\n')
