# THEIR instructions (bio-causal-genomics-pleiotropy-detection, AIPOCH SKILL.md), code blocks applied verbatim to dat.
# Only additions: read dat from CSV, wrap each block in tryCatch to record failures, seed for reproducibility.
NB <- as.integer(Sys.getenv("NB","2000"))  # harness: same PRESSO draw count for both sides (>=1000 is the floor both Skills state); their text says 5000, ours 5000/10000
args <- commandArgs(TRUE); ds <- args[1]
suppressMessages({library(TwoSampleMR); library(MRPRESSO)})
dat <- read.csv(file.path("F:/OpenScience/comparisons/pleiotropy-same-id/run/data", paste0(ds, ".csv")), stringsAsFactors = FALSE)
res <- list(); err <- list()
try_ <- function(name, expr) { tryCatch({ res[[name]] <<- eval.parent(substitute(expr)) }, error = function(e) { err[[name]] <<- conditionMessage(e); cat("ERROR in", name, ":", conditionMessage(e), "\n") }) }
set.seed(1)

# ---- SKILL.md "MR-PRESSO" block ----
try_("presso_block", {
  presso_input <- data.frame(bx = dat$beta.exposure, by = dat$beta.outcome, bxse = dat$se.exposure, byse = dat$se.outcome)
  presso_result <- mr_presso(BetaOutcome = 'by', BetaExposure = 'bx', SdOutcome = 'byse', SdExposure = 'bxse',
    OUTLIERtest = TRUE, DISTORTIONtest = TRUE, data = presso_input, NbDistribution = NB, SignifThreshold = 0.05)
  global_p <- presso_result$`MR-PRESSO results`$`Global Test`$Pvalue
  cat('Global test p-value:', global_p, '\n')
  outliers <- presso_result$`MR-PRESSO results`$`Outlier Test`
  cat('\nOutlier test results (str of Pvalue col):\n'); str(outliers$Pvalue)
  outlier_indices <- which(outliers$Pvalue < 0.05)           # verbatim
  cat('Outlier SNPs:', length(outlier_indices), '\n')
  distortion_p <- presso_result$`MR-PRESSO results`$`Distortion Test`$Pvalue
  cat('Distortion test p-value:', distortion_p, '\n')
  main_results <- presso_result$`Main MR results`
  cat('Raw IVW estimate:', main_results$`Causal Estimate`[1], '\n')
  cat('Corrected IVW estimate:', main_results$`Causal Estimate`[2], '\n')
  list(global_p = global_p, outlier_idx = outlier_indices, distortion_p = distortion_p,
       raw = main_results$`Causal Estimate`[1], corrected = main_results$`Causal Estimate`[2], presso = presso_result)
})

# ---- SKILL.md "MR-Egger Diagnostics" block ----
try_("egger_block", {
  egger <- mr_egger_regression(dat$beta.exposure, dat$beta.outcome, dat$se.exposure, dat$se.outcome)
  cat('Egger intercept:', round(egger$b_i, 5), ' SE:', round(egger$se_i, 5), ' p:', format.pval(egger$pval_i), '\n')
  cat('Egger causal estimate:', round(egger$b, 4), ' SE:', round(egger$se, 4), ' p:', format.pval(egger$pval), '\n')
  isq <- Isq(dat$beta.exposure, dat$se.exposure)
  cat('I-squared:', round(isq, 3), '\n')
  if (isq < 0.9) cat('Warning: I-squared < 0.9\n')
  list(b_i = egger$b_i, se_i = egger$se_i, p_i = egger$pval_i, b = egger$b, se = egger$se, p = egger$pval, isq = isq)
})

# ---- SKILL.md "Steiger Filtering" block ----
try_("steiger_block", {
  steiger <- steiger_filtering(dat)
  dat_steiger <- steiger[steiger$steiger_dir == TRUE, ]
  cat('Instruments passing Steiger filter:', nrow(dat_steiger), 'of', nrow(steiger), '\n')
  results_steiger <- mr(dat_steiger); print(results_steiger[, c('method', 'nsnp', 'b', 'se', 'pval')])
  direction <- directionality_test(dat)
  cat('Correct causal direction:', direction$correct_causal_direction, ' Steiger p:', format.pval(direction$steiger_pval), '\n')
  list(n_pass = nrow(dat_steiger), correct = direction$correct_causal_direction)
})

# ---- SKILL.md "Additional Sensitivity Methods" block ----
try_("conmix_line", { mr_conmix <- mr(dat, method_list = 'mr_raps'); print(mr_conmix[, c('method','b','se','pval')]); mr_conmix })
try_("raps_block", {
  library(MendelianRandomization)
  mr_input <- mr_input(bx = dat$beta.exposure, bxse = dat$se.exposure, by = dat$beta.outcome, byse = dat$se.outcome)
  raps_result <- mr_raps(mr_input)                       # verbatim
  cat('MR-RAPS estimate:', raps_result$Estimate, '\n'); raps_result
})

# ---- SKILL.md "Comprehensive Sensitivity Framework" block ----
try_("battery", {
  run_sensitivity <- function(dat) {
    results <- list()
    results$ivw <- mr(dat, method_list = 'mr_ivw')
    results$egger <- mr(dat, method_list = 'mr_egger_regression')
    results$median <- mr(dat, method_list = 'mr_weighted_median')
    results$mode <- mr(dat, method_list = 'mr_weighted_mode')
    results$het <- mr_heterogeneity(dat)
    results$pleio <- mr_pleiotropy_test(dat)
    results$loo <- mr_leaveoneout(dat)
    presso_input <- data.frame(bx = dat$beta.exposure, by = dat$beta.outcome, bxse = dat$se.exposure, byse = dat$se.outcome)
    results$presso <- mr_presso(BetaOutcome = 'by', BetaExposure = 'bx', SdOutcome = 'byse', SdExposure = 'bxse',
      OUTLIERtest = TRUE, DISTORTIONtest = TRUE, data = presso_input, NbDistribution = NB, SignifThreshold = 0.05)
    results
  }
  summarize_sensitivity <- function(sens) {
    cat('=== MR Sensitivity Analysis Summary ===\n')
    all_mr <- rbind(sens$ivw, sens$egger, sens$median, sens$mode)
    print(all_mr[, c('method', 'b', 'se', 'pval')])
    cat('  Q p-value (IVW):', sens$het$Q_pval[sens$het$method == 'Inverse variance weighted'], '\n')
    cat('  Egger intercept:', sens$pleio$egger_intercept, ' P:', sens$pleio$pval, '\n')
    cat('  MR-PRESSO global p:', sens$presso$`MR-PRESSO results`$`Global Test`$Pvalue, '\n')
    cat('--- Interpretation (verbatim text) ---\n')
    cat('Consistent estimates across methods: Evidence strengthened\n')
    cat('Significant Egger intercept: Directional pleiotropy present\n')
    cat('Significant MR-PRESSO global: Horizontal pleiotropy detected\n')
    cat('Significant heterogeneity: Instruments may be invalid\n')
  }
  sens <- run_sensitivity(dat); summarize_sensitivity(sens)
  list(ivw = sens$ivw$b, egger = sens$egger$b, median = sens$median$b, mode = sens$mode$b,
       q_p = sens$het$Q_pval[sens$het$method == 'Inverse variance weighted'],
       egger_int = sens$pleio$egger_intercept, egger_int_p = sens$pleio$pval,
       presso_global = sens$presso$`MR-PRESSO results`$`Global Test`$Pvalue)
})
saveRDS(list(res = res, err = err), file.path("F:/OpenScience/comparisons/pleiotropy-same-id/run/out", paste0("theirs_", ds, ".rds")))
cat("\nERRORS:", paste(names(err), collapse = ","), "\n")
