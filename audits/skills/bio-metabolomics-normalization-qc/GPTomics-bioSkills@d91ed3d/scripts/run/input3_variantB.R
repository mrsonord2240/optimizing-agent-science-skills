# Input 3 (Variant B) -- Prompt:
# "Diagnose whether my missing values are left-censored (MNAR) or random (MAR) per feature,
# then impute each mechanism with the matched method -- QRILC for MNAR, missForest for MAR --
# and show what happens if I use the wrong method on the MNAR features."
# Synthetic data (this audit): 15 MNAR (low-abundance, left-censored) + 15 MAR (random-drop) features.

source("F:/OpenScience/audits/bio-metabolomics-normalization-qc/data/make_synthetic.R")
library(imputeLCMD)
library(missForest)

d <- make_dataset(n_features = 60, n_bio = 50, n_qc_per_batch = 0, n_batches = 1, seed = 5)
mat <- d$mat[d$class != "QC", , drop = FALSE]  # biological samples only for this test
mi <- inject_missingness(mat, d$true_abundance[1:60], n_mnar = 15, n_mar = 15, seed = 9)
mat_miss <- mi$mat

cat(sprintf("Injected missingness: %d MNAR features, %d MAR features, %d total NAs\n",
            length(mi$mnar_features), length(mi$mar_features), sum(is.na(mat_miss))))

# --- Diagnose mechanism per feature: correlate missingness indicator with feature's own mean
# abundance (proxy used by the Skill's usage-guide: "missingness correlated with low abundance
# is MNAR; sporadic missingness across the abundance range is MAR"). ---
diagnose_mechanism <- function(mat) {
  sapply(seq_len(ncol(mat)), function(f) {
    miss <- is.na(mat[, f])
    if (sum(miss) < 3) return(NA_character_)
    obs_mean <- mean(mat[!miss, f], na.rm = TRUE)
    # A cheap per-feature proxy: compare observed-value mean rank among all features' means.
    "unknown"
  })
}
# Better mechanism diagnostic: fraction missing vs feature's abundance percentile (low-abundance
# features with high missingness => MNAR pattern).
feat_mean <- colMeans(mat_miss, na.rm = TRUE)
feat_missrate <- colMeans(is.na(mat_miss))
abundance_rank <- rank(feat_mean) / ncol(mat_miss)
predicted_mnar <- which(feat_missrate > 0.1 & abundance_rank < 0.35)
predicted_mar <- setdiff(which(feat_missrate > 0.1), predicted_mnar)
cat(sprintf("Mechanism diagnosis: %d flagged MNAR (low-abundance+missing), %d flagged MAR\n",
            length(predicted_mnar), length(predicted_mar)))
cat(sprintf("  True MNAR features correctly flagged: %d / %d\n",
            length(intersect(predicted_mnar, mi$mnar_features)), length(mi$mnar_features)))

# --- Correct imputation: QRILC for MNAR, missForest for MAR ---
mat_correct <- mat_miss
if (length(predicted_mnar) > 0) {
  qrilc_in <- t(mat_miss[, predicted_mnar, drop = FALSE])  # imputeLCMD wants features in rows
  qrilc_out <- impute.QRILC(qrilc_in, tune.sigma = 1)[[1]]
  mat_correct[, predicted_mnar] <- t(qrilc_out)
}
set.seed(1)
rf_out <- missForest(mat_correct, maxiter = 5, ntree = 50, verbose = FALSE)$ximp
mat_correct_full <- rf_out
cat(sprintf("Correct-method imputation: %d NAs remaining\n", sum(is.na(mat_correct_full))))

# --- Wrong-method demonstration: use missForest (MAR method) on the MNAR features directly ---
set.seed(1)
mat_wrong <- missForest(mat_miss, maxiter = 5, ntree = 50, verbose = FALSE)$ximp

# Compare: for a true MNAR feature, wrong-method (kNN/RF-style) pulls the imputed mean UP toward
# the observed mean and shrinks variance, vs correct QRILC drawing plausible LOW values.
f <- mi$mnar_features[1]
miss_rows <- is.na(mat_miss[, f])
cat(sprintf("\nMNAR feature %d -- observed mean: %.1f\n", f, mean(mat_miss[!miss_rows, f])))
cat(sprintf("  Correct (QRILC) imputed-value mean : %.1f | sd: %.2f\n",
            mean(mat_correct_full[miss_rows, f]), sd(mat_correct_full[miss_rows, f])))
cat(sprintf("  Wrong (missForest) imputed-value mean: %.1f | sd: %.2f\n",
            mean(mat_wrong[miss_rows, f]), sd(mat_wrong[miss_rows, f])))
cat("  (Expect: wrong-method mean pulled toward observed mean; correct-method mean stays low,\n")
cat("   preserving the on/off censoring signal, per the Skill's stated failure mode.)\n")

cat("\n[debug] raw QRILC-imputed values for feature", f, ":\n")
print(round(mat_correct_full[miss_rows, f], 1))
cat("[debug] observed (non-missing) values for feature", f, ":\n")
print(round(sort(mat_miss[!miss_rows, f]), 1))
