library(TwoSampleMR)
set.seed(3)
n <- 20
beta_exp <- rnorm(n, 0.05, 0.02); se_exp <- runif(n, 0.005, 0.012)
beta_out <- beta_exp * 0.3 + rnorm(n, 0, 0.01); se_out <- runif(n, 0.008, 0.02)
dat <- data.frame(beta.exposure=beta_exp, se.exposure=se_exp, beta.outcome=beta_out, se.outcome=se_out)
t0 <- Sys.time()
presso <- MRPRESSO::mr_presso(BetaOutcome='beta.outcome', BetaExposure='beta.exposure',
  SdOutcome='se.outcome', SdExposure='se.exposure', OUTLIERtest=TRUE, DISTORTIONtest=TRUE,
  data=dat, NbDistribution=300, SignifThreshold=0.05)
cat('Elapsed:', as.numeric(Sys.time()-t0, units='secs'), 'sec\n')
cat('Global p:', signif(presso$`MR-PRESSO results`$`Global Test`$Pvalue,3), '\n')
cat('MIN_CHECK_DONE\n')
