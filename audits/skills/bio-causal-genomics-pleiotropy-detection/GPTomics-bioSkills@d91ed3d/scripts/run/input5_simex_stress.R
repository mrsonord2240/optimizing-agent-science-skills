# Input 5 (Stress / multi-part) -- "My I^2_GX is around 0.75 -- apply SIMEX to my
# MR-Egger; also run the contamination-mixture method and build a STROBE-MR
# reporting table combining everything." Multi-part request chaining several
# sections of SKILL.md: NOME/I^2_GX check -> SIMEX (examples/simex_egger_correction.R
# pattern) -> MendelianRandomization::mr_conmix -> STROBE-MR summary table.

library(TwoSampleMR)
library(simex)
library(MendelianRandomization)

dat <- readRDS('F:/OpenScience/audits/bio-causal-genomics-pleiotropy-detection/data/synth_simex.rds')

isq <- Isq(dat$beta.exposure, dat$se.exposure)
cat('I^2_GX:', round(isq, 3), '\n')

if (isq < 0.6) {
  cat('NOME severely violated; drop Egger; use MR-RAPS or CAUSE\n')
} else if (isq < 0.9) {
  cat('NOME partially violated; applying SIMEX correction (SKILL.md examples/simex_egger_correction.R pattern)\n')

  # NOTE (audit finding, see debug_simex.R): SKILL.md / examples/simex_egger_correction.R
  # use `weights = 1 / se.outcome^2` computed IN the lm() formula. That exact pattern
  # crashes inside simex()'s internal refit with "object 'se.outcome' not found" --
  # confirmed reproducible, see debug_simex.R. Workaround used here: precompute the
  # weights vector before calling lm(). This is not what SKILL.md tells the agent to
  # write; it is the audit's fix so the rest of the stress input can still execute.
  w <- 1 / dat$se.outcome^2
  egger_lm <- lm(beta.outcome ~ beta.exposure, weights = w, data = dat, x = TRUE, y = TRUE)

  egger_simex <- simex(model = egger_lm, SIMEXvariable = 'beta.exposure',
                        measurement.error = dat$se.exposure,
                        lambda = seq(0.5, 2, 0.5), B = 200,
                        fitting.method = 'quadratic', asymptotic = FALSE)

  naive_slope <- coef(egger_lm)['beta.exposure']
  simex_slope <- coef(egger_simex)['beta.exposure']
  cat('Naive Egger slope:', round(naive_slope, 4), '\n')
  cat('SIMEX-corrected slope:', round(simex_slope, 4), '\n')
  cat('Ground truth causal effect: 0.3\n')
} else {
  cat('NOME severely violated (I^2_GX < 0.6); per SKILL.md, drop Egger entirely -- use MR-RAPS or CAUSE instead.\n')
  cat('(SIMEX is documented as unreliable below 0.6; not attempted.)\n')
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
