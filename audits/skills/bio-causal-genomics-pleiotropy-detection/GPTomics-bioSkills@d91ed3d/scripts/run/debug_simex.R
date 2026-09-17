library(simex)
dat <- readRDS('F:/OpenScience/audits/bio-causal-genomics-pleiotropy-detection/data/synth_simex.rds')

cat('--- Exact SKILL.md / examples/simex_egger_correction.R pattern ---\n')
egger_lm <- lm(beta.outcome ~ beta.exposure,
               weights = 1 / se.outcome^2, data = dat,
               x = TRUE, y = TRUE)
res <- tryCatch({
  simex(model = egger_lm, SIMEXvariable = 'beta.exposure',
        measurement.error = dat$se.exposure,
        lambda = seq(0.5, 2, 0.5), B = 200,
        fitting.method = 'quadratic', asymptotic = FALSE)
}, error = function(e) { cat('FAILS as shipped:', conditionMessage(e), '\n'); NULL })

cat('\n--- Workaround: precompute weights vector instead of in-formula division ---\n')
w <- 1 / dat$se.outcome^2
egger_lm2 <- lm(beta.outcome ~ beta.exposure, weights = w, data = dat, x = TRUE, y = TRUE)
res2 <- tryCatch({
  simex(model = egger_lm2, SIMEXvariable = 'beta.exposure',
        measurement.error = dat$se.exposure,
        lambda = seq(0.5, 2, 0.5), B = 200,
        fitting.method = 'quadratic', asymptotic = FALSE)
}, error = function(e) { cat('Workaround also fails:', conditionMessage(e), '\n'); NULL })
if (!is.null(res2)) {
  cat('Workaround SUCCEEDS. SIMEX-corrected slope:', round(coef(res2)['beta.exposure'], 4), '\n')
  cat('Naive Egger slope:', round(coef(egger_lm2)['beta.exposure'], 4), '\n')
  cat('Ground truth: 0.3\n')
}
