library(simex)
set.seed(55)
n_snps <- 40
beta_exp <- rnorm(n_snps, 0.05, 0.015)
se_exp <- runif(n_snps, 0.02, 0.035)
true_beta_xy <- 0.4
beta_out <- true_beta_xy * beta_exp + 0.02 + rnorm(n_snps, 0, 0.01)
se_out <- runif(n_snps, 0.015, 0.03)
dat <- data.frame(beta.exposure=beta_exp, se.exposure=se_exp, beta.outcome=beta_out, se.outcome=se_out)
egger_lm <- lm(beta.outcome ~ beta.exposure, weights = 1/se.outcome^2, data = dat, x = TRUE, y = TRUE)
res <- tryCatch({
  simex(egger_lm, SIMEXvariable='beta.exposure', measurement.error=dat$se.exposure, fitting.method='quad', asymptotic=FALSE)
}, error=function(e) { cat('CRASH:', conditionMessage(e), '\n'); NULL })
if(!is.null(res)) cat('SUCCEEDED (unsafe bare-name weights pattern)\n')
