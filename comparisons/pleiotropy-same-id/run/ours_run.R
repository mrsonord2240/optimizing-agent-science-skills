# OUR instructions (shelf SKILL.md "Standard Sensitivity Battery (Working Reference)" block) applied verbatim to dat.
# Only additions: read dat from CSV, tryCatch, saving results, and printing the values the request asks for.
NB <- as.integer(Sys.getenv("NB","2000"))  # harness: same PRESSO draw count for both sides (>=1000 is the floor both Skills state); their text says 5000, ours 5000/10000
args <- commandArgs(TRUE); ds <- args[1]
suppressMessages({library(TwoSampleMR); library(MRPRESSO)})
dat <- read.csv(file.path("F:/OpenScience/comparisons/pleiotropy-same-id/run/data", paste0(ds, ".csv")), stringsAsFactors = FALSE)
res <- list(); err <- list()
tryCatch({
  # ---- verbatim from SKILL.md ----
  methods <- c('mr_ivw', 'mr_egger_regression', 'mr_weighted_median', 'mr_weighted_mode')
  res_mr <- mr(dat, method_list = methods)
  het <- mr_heterogeneity(dat)
  pleio <- mr_pleiotropy_test(dat)
  loo <- mr_leaveoneout(dat)
  steiger <- directionality_test(dat)
  isq <- Isq(dat$beta.exposure, dat$se.exposure)
  nome_pass <- isq >= 0.9
  set.seed(42)
  presso <- mr_presso(BetaOutcome='beta.outcome', BetaExposure='beta.exposure', SdOutcome='se.outcome', SdExposure='se.exposure',
    OUTLIERtest=TRUE, DISTORTIONtest=TRUE, data=dat, NbDistribution=NB, SignifThreshold=0.05)
  global_p <- presso$`MR-PRESSO results`$`Global Test`$Pvalue
  outlier_p <- presso$`MR-PRESSO results`$`Outlier Test`$Pvalue
  distortion_p <- presso$`MR-PRESSO results`$`Distortion Test`$Pvalue
  n_outliers <- sum(outlier_p < 0.05, na.rm=TRUE)
  # ---- end verbatim ----
  print(res_mr[, c('method','nsnp','b','se','pval')]); print(het[, c('method','Q','Q_df','Q_pval')])
  cat('Egger intercept:', pleio$egger_intercept, 'SE', pleio$se, 'p', pleio$pval, '\n')
  cat('I2_GX', isq, 'NOME pass', nome_pass, '\n'); print(steiger)
  cat('PRESSO global p', global_p, ' n_outliers', n_outliers, ' distortion p', distortion_p, '\n')
  str(outlier_p)
  main <- presso$`Main MR results`; print(main)
  res <- list(ivw = res_mr$b[1], egger = res_mr$b[2], median = res_mr$b[3], mode = res_mr$b[4],
    q_p = het$Q_pval[het$method == 'Inverse variance weighted'], egger_int = pleio$egger_intercept, egger_int_p = pleio$pval,
    isq = isq, global_p = global_p, outlier_idx = which(outlier_p < 0.05), n_outliers = n_outliers, distortion_p = distortion_p,
    raw = main$`Causal Estimate`[1], corrected = main$`Causal Estimate`[2], steiger_correct = steiger$correct_causal_direction)
}, error = function(e) { err$main <<- conditionMessage(e); cat("ERROR:", conditionMessage(e), "\n") })
saveRDS(list(res = res, err = err), file.path("F:/OpenScience/comparisons/pleiotropy-same-id/run/out", paste0("ours_", ds, ".rds")))
