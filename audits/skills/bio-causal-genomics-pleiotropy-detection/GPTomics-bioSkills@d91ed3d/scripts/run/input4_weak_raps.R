# Input 4 (Variant B) -- "My instruments are mostly weak (mean F < 20, maybe much
# lower). Use MR-RAPS with Huber robust loss and overdispersion modeling instead of
# IVW; report point estimate and CI alongside IVW." Ground truth causal effect = 0.25.
# Now executable for real: mr.raps 0.4.3 and TwoSampleMR::mr_raps() both confirmed
# working in this environment (see TOOLS.md core table, resolved after the tooling
# session ended).

library(TwoSampleMR)

dat <- readRDS('F:/OpenScience/audits/bio-causal-genomics-pleiotropy-detection/data/synth_weak.rds')
f <- (dat$beta.exposure / dat$se.exposure)^2
cat('Mean F:', round(mean(f), 2), ' (SKILL.md: <10 = weak) | ground truth causal effect = 0.25\n\n')

cat('=== IVW (naive) ===\n')
res_ivw <- mr(dat, method_list = c('mr_ivw'))
print(res_ivw[, c('method','nsnp','b','se','pval')])

cat('\n=== MR-RAPS, over.dispersion=TRUE, loss.function=huber (SKILL.md defaults) ===\n')
raps <- TwoSampleMR::mr_raps(b_exp = dat$beta.exposure, b_out = dat$beta.outcome,
                              se_exp = dat$se.exposure, se_out = dat$se.outcome,
                              parameters = list(over.dispersion = TRUE, loss.function = 'huber', shrinkage = FALSE))
cat('RAPS b:', round(raps$b, 4), ' se:', round(raps$se, 4), ' p:', format.pval(raps$pval), ' nsnp:', raps$nsnp, '\n')

cat('\n=== MR-RAPS, loss.function=tukey (more aggressive) ===\n')
raps_tukey <- TwoSampleMR::mr_raps(b_exp = dat$beta.exposure, b_out = dat$beta.outcome,
                                    se_exp = dat$se.exposure, se_out = dat$se.outcome,
                                    parameters = list(over.dispersion = TRUE, loss.function = 'tukey', shrinkage = FALSE))
cat('RAPS(tukey) b:', round(raps_tukey$b, 4), ' se:', round(raps_tukey$se, 4), '\n')

cat('\n=== Comparison against ground truth (0.25) ===\n')
cat('IVW error:', round(abs(res_ivw$b[1] - 0.25), 4), '   RAPS(huber) error:', round(abs(raps$b - 0.25), 4), '\n')
