# Input 3 (Edge) -- Sparse instrument set: only 3 genome-wide-significant cis-instruments
# survive for a protein exposure on a disease outcome. SKILL.md's Common Errors table says
# "MR-PRESSO returns NA p-value | NbDistribution too small; signal too thin | ... check that
# >= 4 SNPs remain after harmonization" -- this is a 3-SNP set, one below that floor.
# Also below Egger's stated >=10 SNP power floor. Correct behavior per SKILL.md: IVW/Wald-ratio
# only, do not force Egger/PRESSO, and where power is this thin recommend colocalization instead
# (Related Skills: colocalization-analysis).

library(TwoSampleMR)

set.seed(99)
true_beta_xy <- 0.35
n_snps <- 3

exp_dat <- data.frame(
  SNP = paste0('rs', 1:n_snps),
  beta.exposure = c(0.22, 0.18, 0.30),
  se.exposure = c(0.03, 0.025, 0.035),
  effect_allele.exposure = c('A', 'C', 'G'),
  other_allele.exposure = c('G', 'T', 'A'),
  eaf.exposure = c(0.30, 0.55, 0.40),
  pval.exposure = c(1e-12, 5e-10, 1e-15),
  exposure = 'Protein P (cis-pQTL)', id.exposure = 'ProtP', mr_keep.exposure = TRUE
)
exp_dat$f_stat <- (exp_dat$beta.exposure / exp_dat$se.exposure)^2
cat('F-statistics:', round(exp_dat$f_stat, 1), '\n')

out_dat <- data.frame(
  SNP = exp_dat$SNP,
  beta.outcome = exp_dat$beta.exposure * true_beta_xy + c(0.01, -0.005, 0.008),
  se.outcome = c(0.04, 0.05, 0.045),
  effect_allele.outcome = exp_dat$effect_allele.exposure,
  other_allele.outcome = exp_dat$other_allele.exposure,
  eaf.outcome = exp_dat$eaf.exposure,
  pval.outcome = c(0.02, 0.15, 0.01),
  outcome = 'Disease D', id.outcome = 'DiseaseD', mr_keep.outcome = TRUE
)

dat <- harmonise_data(exp_dat, out_dat, action = 2)
cat('SNPs after harmonisation:', sum(dat$mr_keep), '\n')
dat <- dat[dat$mr_keep, ]

ivw <- mr(dat, method_list = 'mr_ivw')
cat('\n--- IVW (3 SNPs) ---\n')
print(ivw[, c('method', 'nsnp', 'b', 'se', 'pval')])
cat('True causal beta_XY was:', true_beta_xy, '\n')

cat('\n--- Attempting Egger anyway (SKILL.md: needs >=10 SNPs for power) ---\n')
egger <- tryCatch(mr(dat, method_list = 'mr_egger_regression'),
                   error = function(e) { cat('Egger ERROR:', conditionMessage(e), '\n'); NULL })
if (!is.null(egger)) print(egger[, c('method', 'nsnp', 'b', 'se', 'pval')])

cat('\n--- Attempting MR-PRESSO (SKILL.md Common Errors: needs >=4 SNPs after harmonisation) ---\n')
presso <- tryCatch(
  MRPRESSO::mr_presso(
    BetaOutcome = 'beta.outcome', BetaExposure = 'beta.exposure',
    SdOutcome = 'se.outcome', SdExposure = 'se.exposure',
    OUTLIERtest = TRUE, DISTORTIONtest = TRUE,
    data = dat, NbDistribution = 1000, SignifThreshold = 0.05
  ),
  error = function(e) { cat('MR-PRESSO ERROR (expected per SKILL.md):', conditionMessage(e), '\n'); NULL }
)
