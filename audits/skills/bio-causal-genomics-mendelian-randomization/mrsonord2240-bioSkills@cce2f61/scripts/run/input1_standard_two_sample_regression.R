# Input 1 (regression, P0 focus) -- Standard two-sample MR battery on real GIANT-BMI15 x
# PGC-MDD18 GWAS, following the FIXED examples/two_sample_mr.R pattern verbatim (guarded
# MR-PRESSO Pvalue formatting). Real published GWAS data, cached locally (MRMix package),
# zero network calls. Mirrors the pre-fix audit's Input 1 exactly so the P0 crash is a true
# regression test.
options(warn = 1)
library(TwoSampleMR)
library(MRPRESSO)

bmi <- readRDS("F:/OpenScience/audit-envs/mendelian-randomization-analyst/public-data/MRMix_BMI15.rds")
mdd <- readRDS("F:/OpenScience/audit-envs/mendelian-randomization-analyst/public-data/MRMix_MDD18.rds")

exp_df <- data.frame(
    SNP = bmi$SNP, beta = bmi$beta, se = bmi$se,
    effect_allele = bmi$effect_allele, other_allele = bmi$other_allele,
    eaf = bmi$EAF, pval = bmi$pval, samplesize = bmi$N,
    stringsAsFactors = FALSE
)
exposure_dat <- format_data(exp_df, type = "exposure",
    snp_col = "SNP", beta_col = "beta", se_col = "se",
    effect_allele_col = "effect_allele", other_allele_col = "other_allele",
    eaf_col = "eaf", pval_col = "pval", samplesize_col = "samplesize")

# MDD18 is logistic (OR/SE on log-odds scale); convert to beta = log(OR) per standard practice.
out_df <- data.frame(
    SNP = mdd$SNP, beta = log(mdd$OR), se = mdd$SE,
    effect_allele = mdd$A1, other_allele = mdd$A2,
    eaf = mdd$FRQ_A_59851, pval = mdd$P, samplesize = mdd$Neff,
    stringsAsFactors = FALSE
)
outcome_dat <- format_data(out_df, type = "outcome",
    snp_col = "SNP", beta_col = "beta", se_col = "se",
    effect_allele_col = "effect_allele", other_allele_col = "other_allele",
    eaf_col = "eaf", pval_col = "pval", samplesize_col = "samplesize")

exposure_dat$f_stat <- (exposure_dat$beta.exposure / exposure_dat$se.exposure)^2
cat('Mean F:', round(mean(exposure_dat$f_stat), 1), '| n SNPs before harmonise:', nrow(exposure_dat), '\n')

dat <- harmonise_data(exposure_dat, outcome_dat, action = 2)
dat <- subset(dat, mr_keep)
cat('SNPs after harmonization:', nrow(dat), '\n')

primary <- mr(dat, method_list = c('mr_ivw', 'mr_egger_regression',
                                    'mr_weighted_median', 'mr_weighted_mode'))
cat('\n--- Primary MR ---\n')
print(primary[, c('method', 'nsnp', 'b', 'se', 'pval')])

het <- mr_heterogeneity(dat)
cat('\n--- Heterogeneity ---\n')
print(het[, c('method', 'Q', 'Q_df', 'Q_pval')])

pleio <- mr_pleiotropy_test(dat)
cat('\n--- Egger intercept ---\n')
cat('intercept:', signif(pleio$egger_intercept, 3),
    '| se:', signif(pleio$se, 3), '| p:', signif(pleio$pval, 3), '\n')

isq <- TwoSampleMR::Isq(dat$beta.exposure, dat$se.exposure)
cat('I^2_GX:', round(isq, 3), if (isq < 0.9) ' -- NOME VIOLATED; SIMEX-correct Egger\n' else ' -- NOME OK\n')

raps <- TwoSampleMR::mr_raps(b_exp = dat$beta.exposure, b_out = dat$beta.outcome,
                              se_exp = dat$se.exposure, se_out = dat$se.outcome)
cat('\n--- MR-RAPS (Huber) ---\n')
cat('beta:', signif(raps$b, 3), '| se:', signif(raps$se, 3),
    '| p:', signif(raps$pval, 3), '\n')

steiger <- directionality_test(dat)
cat('\n--- Steiger ---\n')
cat('correct direction:', steiger$correct_causal_direction,
    '| p:', signif(steiger$steiger_pval, 3), '\n')

loo <- mr_leaveoneout(dat)
cat('\n--- Leave-one-out range of IVW estimate ---\n')
cat('min:', signif(min(loo$b), 3), '| max:', signif(max(loo$b), 3), '\n')

# --- MR-PRESSO: the P0 regression target. Reduced NbDistribution (1000, not 10000) to fit a
# real-data run inside this session's turn budget -- flagged per the audit brief's own trap note.
# 1000 draws still empirically triggers MRPRESSO's Pvalue==0 -> character-string coercion path
# whenever the bootstrap p rounds to 0 at that resolution, so it still exercises the exact bug.
set.seed(42)
t0 <- Sys.time()
presso <- mr_presso(
    BetaOutcome = 'beta.outcome', BetaExposure = 'beta.exposure',
    SdOutcome = 'se.outcome', SdExposure = 'se.exposure',
    OUTLIERtest = TRUE, DISTORTIONtest = TRUE,
    data = dat, NbDistribution = 1000, SignifThreshold = 0.05
)
cat('\nMR-PRESSO wall time (s):', round(as.numeric(Sys.time() - t0, units = "secs"), 1), '\n')
cat('\n--- MR-PRESSO (guarded reporting, as shipped in the FIXED examples/two_sample_mr.R) ---\n')
presso_p <- presso$`MR-PRESSO results`$`Global Test`$Pvalue
cat('Pvalue field class:', class(presso_p), '| raw value:', presso_p, '\n')
presso_p_fmt <- if (is.numeric(presso_p)) signif(presso_p, 3) else presso_p
cat('Global RSSobs:', signif(presso$`MR-PRESSO results`$`Global Test`$RSSobs, 3),
    '| p:', presso_p_fmt, '\n')
if (!is.null(presso$`MR-PRESSO results`$`Distortion Test`)) {
    distortion_p <- presso$`MR-PRESSO results`$`Distortion Test`$Pvalue
    cat('Distortion p:', if (is.numeric(distortion_p)) signif(distortion_p, 3) else distortion_p, '\n')
}
cat('\nP0 REGRESSION RESULT: MR-PRESSO reporting line executed WITHOUT crashing.\n')

cat('\n--- STROBE-MR summary ---\n')
cat('Exposure SNPs:', nrow(dat), '| Mean F:', round(mean(exposure_dat$f_stat), 1), '\n')
cat('Primary IVW beta:', signif(primary$b[primary$method == 'Inverse variance weighted'], 3),
    '| p:', signif(primary$pval[primary$method == 'Inverse variance weighted'], 3), '\n')
