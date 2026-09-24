# THEIRS request 5: "decompose the effect into direct / indirect / interaction parts" on dataset D (interaction planted).
# THEIR SKILL.md only offers mediation::mediate (Basic Mediation block, no interaction term): run that as written.
source('F:/OpenScience/comparisons/mediation-same-id/run/common.R'); suppressMessages(library(mediation))
dat <- read.csv(file.path(D, 'D_interaction.csv')); set.seed(1)
mm <- lm(expression ~ genotype + age + sex, data = dat)
om <- lm(y_cont ~ genotype + expression + age + sex, data = dat)   # as their block: no G*M term
r <- mediate(mm, om, treat = 'genotype', mediator = 'expression', boot = TRUE, sims = 1000)
cat('THEIR block: ACME', round(r$d0, 3), 'ADE', round(r$z0, 3), 'Total', round(r$tau.coef, 3), 'PM', round(r$n0, 3), '\n')
cat('components reported: ACME, ADE, total, PM only (no CDE/INTref/INTmed/PIE split)\n')
cat('TRUTH: CDE 0.2, INTref 0, INTmed 0.2, PIE 0.3, TE 0.7 ; natural indirect: 0.3 (at G=0), 0.5 (at G=1)\n')
cat('THEIR interpretation: ACME 0.3-ish with ADE ', round(r$z0, 3), ' vs truth ADE-at-M(0) 0.2 / total 0.7\n')
cat('Is the interaction visible anywhere in their output? outcome-model has no G:M term -> NA\n')
cat('Total effect estimate vs truth 0.7:', round(r$tau.coef, 3), '\n')
stopifnot(abs(r$tau.coef - 0.7) < 0.1); cat('ASSERT pass: total effect ~0.7\n')
# what would the truth of their two ACMEs be? assert their single ACME hides the split
cat('ACME treated', round(r$d1, 3), 'control', round(r$d0, 3), '(they differ by INTmed only if the model has the interaction; here both come from a main-effects model)\n')
