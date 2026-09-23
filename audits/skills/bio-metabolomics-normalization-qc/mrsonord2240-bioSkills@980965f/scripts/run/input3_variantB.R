# Input 3 (Variant B) -- Prompt:
# "Diagnose whether my missing values are left-censored (MNAR) or random (MAR) per feature,
# then impute each mechanism with the matched method -- QRILC for MNAR, missForest for MAR --
# and show what happens if I use the wrong method on the MNAR features."
# REGRESSION TEST (post-fix): this is the P0 research-veto input. The fixed SKILL.md's "Impute
# by Missingness Mechanism" section now requires log2() immediately before impute.QRILC and
# 2^x back-transform immediately after, plus a stopifnot(min(...) >= 0) guard. Reproduce the
# EXACT SAME synthetic scenario (seed 5/9) that produced negative values pre-fix and confirm the
# fix holds.

source("F:/OpenScience/audits/bio-metabolomics-normalization-qc/data/make_synthetic.R")
library(imputeLCMD)
library(missForest)

d <- make_dataset(n_features = 60, n_bio = 50, n_qc_per_batch = 0, n_batches = 1, seed = 5)
mat <- d$mat[d$class != "QC", , drop = FALSE]
mi <- inject_missingness(mat, d$true_abundance[1:60], n_mnar = 15, n_mar = 15, seed = 9)
mat_miss <- mi$mat

cat(sprintf("Injected missingness: %d MNAR features, %d MAR features, %d total NAs\n",
            length(mi$mnar_features), length(mi$mar_features), sum(is.na(mat_miss))))

feat_mean <- colMeans(mat_miss, na.rm = TRUE)
feat_missrate <- colMeans(is.na(mat_miss))
abundance_rank <- rank(feat_mean) / ncol(mat_miss)
predicted_mnar <- which(feat_missrate > 0.1 & abundance_rank < 0.35)
predicted_mar <- setdiff(which(feat_missrate > 0.1), predicted_mnar)
cat(sprintf("Mechanism diagnosis: %d flagged MNAR (low-abundance+missing), %d flagged MAR\n",
            length(predicted_mnar), length(predicted_mar)))
cat(sprintf("  True MNAR features correctly flagged: %d / %d\n",
            length(intersect(predicted_mnar, mi$mnar_features)), length(mi$mnar_features)))

# --- FIXED pattern: log2() before impute.QRILC, 2^x back-transform after, stopifnot guard ---
mat_correct <- mat_miss
if (length(predicted_mnar) > 0) {
  qrilc_in <- t(mat_miss[, predicted_mnar, drop = FALSE])   # imputeLCMD wants features in rows
  log_mat <- log2(qrilc_in)
  qrilc_log_out <- impute.QRILC(log_mat, tune.sigma = 1)[[1]]
  qrilc_out <- 2^qrilc_log_out
  stopifnot(min(qrilc_out, na.rm = TRUE) >= 0)
  cat("QRILC negative-value guard: PASS (min imputed value >= 0 on the original scale)\n")
  mat_correct[, predicted_mnar] <- t(qrilc_out)
}
set.seed(1)
rf_out <- missForest(mat_correct, maxiter = 5, ntree = 50, verbose = FALSE)$ximp
mat_correct_full <- rf_out
cat(sprintf("Correct-method imputation: %d NAs remaining\n", sum(is.na(mat_correct_full))))

# --- Wrong-method demonstration (unaffected by the fix): missForest (MAR method) on MNAR features ---
set.seed(1)
mat_wrong <- missForest(mat_miss, maxiter = 5, ntree = 50, verbose = FALSE)$ximp

f <- mi$mnar_features[1]
miss_rows <- is.na(mat_miss[, f])
cat(sprintf("\nMNAR feature %d -- observed mean: %.1f\n", f, mean(mat_miss[!miss_rows, f])))
cat(sprintf("  Correct (log2/QRILC/2^x) imputed-value mean : %.1f | sd: %.2f | min: %.2f\n",
            mean(mat_correct_full[miss_rows, f]), sd(mat_correct_full[miss_rows, f]),
            min(mat_correct_full[miss_rows, f])))
cat(sprintf("  Wrong (missForest) imputed-value mean: %.1f | sd: %.2f\n",
            mean(mat_wrong[miss_rows, f]), sd(mat_wrong[miss_rows, f])))

cat("\n[debug] raw QRILC-imputed values (original scale) for feature", f, ":\n")
print(round(mat_correct_full[miss_rows, f], 1))
cat("[debug] observed (non-missing) values for feature", f, ":\n")
print(round(sort(mat_miss[!miss_rows, f]), 1))
cat(sprintf("\n[debug] fraction of imputed values below the feature's observed min (%.1f): %d / %d\n",
            min(mat_miss[!miss_rows, f]), sum(mat_correct_full[miss_rows, f] < min(mat_miss[!miss_rows, f])),
            sum(miss_rows)))

# --- Whole-matrix check across ALL 15 MNAR features (not just feature 1) ---
all_mnar_imputed <- unlist(lapply(predicted_mnar, function(ff) {
  rows <- is.na(mat_miss[, ff])
  mat_correct_full[rows, ff]
}))
cat(sprintf("\n[whole-matrix] %d total QRILC-path imputed values across %d flagged-MNAR features: min=%.2f, %d negative\n",
            length(all_mnar_imputed), length(predicted_mnar), min(all_mnar_imputed), sum(all_mnar_imputed < 0)))
