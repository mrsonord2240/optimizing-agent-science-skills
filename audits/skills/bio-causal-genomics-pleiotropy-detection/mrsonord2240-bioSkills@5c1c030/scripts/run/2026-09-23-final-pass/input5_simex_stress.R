# Input 5 (Stress / multi-part, REGRESSION of pre-fix Input 5) -- "My I^2_GX is around
# 0.75 -- apply SIMEX to my MR-Egger; also run the contamination-mixture method and
# build a STROBE-MR reporting table combining everything."
#
# THIS IS THE LOAD-BEARING REGRESSION TEST: the pre-fix audit's Research Veto (M4,
# Code Usability) FAILED here because examples/simex_egger_correction.R crashed
# verbatim with "object 'se.outcome' not found". The fix precomputes the weights vector
# before lm() instead of dividing a data-frame column in-formula. This script sources
# the exact audited worktree's examples/simex_egger_correction.R file directly,
# unmodified, exactly as an agent following the Skill would -- no audit-side workaround.

library(TwoSampleMR)
library(simex)
library(MendelianRandomization)

dat <- readRDS('F:/OpenScience/audits/bio-causal-genomics-pleiotropy-detection/data/synth_simex.rds')

isq <- Isq(dat$beta.exposure, dat$se.exposure)
cat('I^2_GX:', round(isq, 3), '(0.6-0.9 band expected -- SIMEX indicated)\n\n')

cat('=== Sourcing the SHIPPED examples/simex_egger_correction.R verbatim ===\n')
result <- tryCatch({
  source('F:/OpenScience/wt/causal-genomics-pleiotropy-detection/causal-genomics/pleiotropy-detection/examples/simex_egger_correction.R')
  'OK'
}, error = function(e) {
  cat('CRASH:', conditionMessage(e), '\n')
  'CRASH'
})
cat('\nShipped example result:', result, '\n')

if (result == 'OK' && exists('egger_simex')) {
  naive_slope <- coef(egger_lm)['beta.exposure']
  simex_slope <- coef(egger_simex)['beta.exposure']
  cat('Naive Egger slope:', round(naive_slope, 4), '\n')
  cat('SIMEX-corrected slope:', round(simex_slope, 4), '\n')
  cat('Ground truth causal effect: 0.3\n')
} else {
  naive_slope <- NA; simex_slope <- NA
}

cat('\n=== Contamination mixture (MendelianRandomization::mr_conmix) ===\n')
mr_obj <- mr_input(bx = dat$beta.exposure, bxse = dat$se.exposure,
                    by = dat$beta.outcome, byse = dat$se.outcome, snps = dat$SNP)
conmix <- mr_conmix(mr_obj)
cat('conmix class:', class(conmix), '\n')
cat('Estimate:', round(conmix@Estimate, 4), '  95% CI:', round(conmix@CILower, 4), 'to', round(conmix@CIUpper, 4), '\n')

cat('\n=== IVW for comparison ===\n')
ivw_res <- mr_ivw(mr_obj)
cat('IVW estimate:', round(ivw_res@Estimate, 4), '\n')

cat('\n=== STROBE-MR style summary table ===\n')
tab <- data.frame(
  Method = c('IVW', 'Egger (naive)', 'Egger (SIMEX)', 'Contamination mixture'),
  Estimate = round(c(ivw_res@Estimate, naive_slope, simex_slope, conmix@Estimate), 4))
print(tab)
cat('Ground truth: 0.3\n')
