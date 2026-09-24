# THEIRS request 2: sequential ignorability violated (dataset B; truth ACME = 0, planted residual rho ~0.237).
# Follows THEIR SKILL.md: Basic Mediation (boot, sims=1000) -> Interpreting Results -> Assumptions and Diagnostics (medsens as written).
source('F:/OpenScience/comparisons/mediation-same-id/run/common.R')
suppressMessages(library(mediation))
dat <- read.csv(file.path(D, 'B_confounded.csv')); set.seed(1)
mm <- lm(expression ~ genotype + age + sex + pc1 + pc2, data = dat)
om <- lm(y_cont ~ genotype + expression + age + sex + pc1 + pc2, data = dat)
r <- try_run('mediate boot sims=1000', mediate(mm, om, treat = 'genotype', mediator = 'expression', boot = TRUE, sims = 1000))
cat('ACME', round(r$d0, 4), 'CI', round(r$d0.ci, 4), 'p', r$d0.p, '| ADE', round(r$z0, 4), '| Total', round(r$tau.coef, 4), '| PM', round(r$n0, 3), '\n')
cat('TRUTH: ACME 0, ADE 0.2, total 0.2; planted rho', round(truth$B$planted_rho, 3), '\n')
cat('THEIR interpretation rules: CI excludes 0 -> "Evidence for mediation": ', r$d0.ci[1] > 0 | r$d0.ci[2] < 0, '; PM>0.2 "Meaningful mediation": ', r$n0 > 0.2, '\n')
cat('--- medsens exactly as their SKILL.md (rho.by=0.1, effect.type indirect, sims=1000) ---\n')
s <- try_run('medsens as written', medsens(r, rho.by = 0.1, effect.type = 'indirect', sims = 1000))
if (is.null(s)) { cat('--- adapt: refit with boot=FALSE (parametric) then medsens ---\n')
  r0 <- mediate(mm, om, treat = 'genotype', mediator = 'expression', boot = FALSE, sims = 1000)
  s <- try_run('medsens boot=FALSE', medsens(r0, rho.by = 0.05, effect.type = 'indirect', sims = 1000)) }
if (!is.null(s)) { print(summary(s)); cat('rho at which ACME=0 (s$rho.by grid):', s$err.cr.d, '\n') }
rho_crit <- if (!is.null(s)) s$err.cr.d else NA
cat('THEIR threshold text: |rho|>0.3 reasonably robust. rho_crit =', round(rho_crit, 3), '->', if (!is.na(rho_crit) && abs(rho_crit) > 0.3) 'labelled ROBUST' else 'not labelled robust', '\n')
saveRDS(list(acme = r$d0, ci = r$d0.ci, rho = rho_crit), file.path(O, 'theirs_r2.rds'))
stopifnot(r$d0.ci[1] > 0)  # assert the spurious-significance premise: naive CI excludes the true 0
cat('ASSERT pass: naive ACME CI excludes truth 0 (i.e. the bootstrap CI alone is wrong)\n')
stopifnot(!is.na(rho_crit), abs(rho_crit - truth$B$planted_rho) < 0.08); cat('ASSERT pass: rho_crit within 0.08 of planted rho\n')
