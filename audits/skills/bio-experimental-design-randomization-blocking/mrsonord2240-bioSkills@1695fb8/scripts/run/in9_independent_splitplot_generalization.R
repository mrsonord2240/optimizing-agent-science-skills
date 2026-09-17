# Input 8 (NEW) -- does the Skill steer to the correct model from a design DESCRIPTION
# alone (never using the words "split-plot" or "whole-plot"), and does the anti-conservative
# claim generalize under an INDEPENDENTLY authored simulation (different scenario, different
# run count, different effect sizes/noise structure than the Skill's own examples/*.R sim)?
#
# Prompt: "I'm testing two growth media (each applied to a whole bioreactor run -- I can only
# run one medium per batch) crossed with two cell lines (both cell lines are seeded into
# multiple flasks within each run). I have 8 bioreactor runs total, 4 flasks per run. What
# model should I fit to test the growth-medium effect?"
#
# Design-recognition check (Mode A, no code): the Skill's own Decision Tree row --
# "One factor fixed per run (incubator temp, sequencing lane) -> split-plot; whole-plot =
# run, sub-plot = sample" -- covers this exactly by structural analogy (medium is fixed per
# bioreactor RUN = whole-plot; cell line varies WITHIN run across flasks = sub-plot), even
# though the prompt never says "split-plot", "whole-plot", "lane", or "incubator". A
# correctly-behaving agent reading only SKILL.md should recognize "one factor applied per
# batch/run, other factor varies within" as the split-plot trigger and recommend
# lmer(growth ~ medium + cell_line + (1 | run)), NOT a flat lm().
#
# Quantitative check: independently simulate this exact bioreactor scenario (8 runs, 4
# flasks/run, medium = whole-plot with true effect 0, cell_line = sub-plot with true effect
# 0.5, between-run SD 2x residual SD -- all different from the Skill's own 6-run/1.5x-SD
# simulation) and confirm the flat-vs-mixed-model Type-I error gap holds under different
# parameters, not just the Skill's own worked numbers.
suppressPackageStartupMessages({
  library(lme4)
  library(lmerTest)
})

n_runs <- 8
n_flasks <- 4
sigma_run <- 1.0     # between-run (whole-plot) SD
sigma_resid <- 0.5   # sigma_run/sigma_resid = 2x, different ratio than the Skill's 1.5/0.5=3x
true_cellline_effect <- 0.5
true_medium_effect <- 0     # null: no real whole-plot effect
nsim <- 400
alpha <- 0.05

one_sim <- function() {
  runs <- data.frame(run = factor(1:n_runs), medium = rep(c('A', 'B'), each = n_runs / 2))
  runs$medium <- sample(runs$medium)
  run_effect <- setNames(rnorm(n_runs, 0, sigma_run), runs$run)
  df <- do.call(rbind, lapply(seq_len(n_runs), function(r) {
    cell_line <- sample(rep(c('L1', 'L2'), each = n_flasks / 2))
    data.frame(run = runs$run[r], medium = runs$medium[r], cell_line = cell_line)
  }))
  df$growth <- true_medium_effect * (df$medium == 'B') +
    true_cellline_effect * (df$cell_line == 'L2') +
    run_effect[df$run] + rnorm(nrow(df), 0, sigma_resid)

  flat  <- lm(growth ~ medium + cell_line, data = df)
  mixed <- suppressWarnings(lmer(growth ~ medium + cell_line + (1 | run), data = df))
  sm <- suppressWarnings(coef(summary(mixed)))
  c(flat = coef(summary(flat))['mediumB', 'Pr(>|t|)'],
    mixed = sm['mediumB', 'Pr(>|t|)'])
}

set.seed(424242)
res <- t(replicate(nsim, one_sim()))
rate_flat  <- mean(res[, 'flat']  < alpha)
rate_mixed <- mean(res[, 'mixed'] < alpha)
cat(sprintf('Independent sim (8 runs, 4 flasks/run, sigma_run/sigma_resid=2x, nsim=%d):\n', nsim))
cat(sprintf('  Flat lm() rejection rate for null whole-plot (medium) effect:  %.3f\n', rate_flat))
cat(sprintf('  Mixed lmer(...+(1|run)) rejection rate:                        %.3f\n', rate_mixed))

stopifnot(
  "flat model must be clearly anti-conservative under an independently chosen scenario" =
    rate_flat > 2 * alpha,
  "mixed model must stay within a reasonable band of nominal alpha" =
    rate_mixed > alpha / 3 && rate_mixed < alpha * 3,
  "flat model's Type-I error must exceed the mixed model's by a clear margin" =
    rate_flat > rate_mixed + 0.05
)
cat('Independent-scenario assertions passed: the anti-conservative claim generalizes.\n')
