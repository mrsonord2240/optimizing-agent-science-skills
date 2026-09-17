library(TwoSampleMR)
set.seed(999)
n <- 20
beta_exposure <- rnorm(n, 0.05, 0.018)
for (se in c(0.005, 0.008, 0.010, 0.012, 0.015, 0.018, 0.020)) {
  se_exposure <- rep(se, n)
  isq <- Isq(beta_exposure, se_exposure)
  cat('se=', se, ' I2_GX=', round(isq,3), '\n')
}
