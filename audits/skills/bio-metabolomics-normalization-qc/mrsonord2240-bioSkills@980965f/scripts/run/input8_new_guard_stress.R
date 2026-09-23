# Input 8 (NEW -- auditor-authored, not in the pre-fix audit) -- Prompt:
# "Our peak table sometimes has a few near-zero or slightly negative values in it after an
# upstream drift-correction step divided by a small trend estimate. Impute the MNAR features
# with QRILC the way your Skill documents it, and tell me if the negative-intensity bug from
# before is really fixed."
#
# Two things this audit's own inputs (1-7, and the fixer's own verification) never tested:
#   (A) Does the new stopifnot guard actually FIRE if an agent reverts to the pre-fix mistake
#       (calling impute.QRILC directly on raw, non-log intensities)? A guard nobody can trip is
#       decoration, not a fix.
#   (B) The fixed pattern is log2()-then-QRILC-then-2^x. log2() of a non-positive raw intensity
#       produces NaN (or -Inf at exactly 0), not a normal negative number. stopifnot(min(x,
#       na.rm=TRUE) >= 0) uses na.rm=TRUE, and is.na(NaN) is TRUE in R -- so NaNs silently drop
#       out of the min() check rather than tripping it. Does the guard catch that, or wave it
#       through with corrupted values left in the output?

source("F:/OpenScience/audits/bio-metabolomics-normalization-qc/data/make_synthetic.R")
library(imputeLCMD)

# Part A reuses input 3's exact known-negative-reproducing scenario (seed 5/9, diagnosed subset)
# -- a first attempt with fresh seeds (77/78) hit an unrelated impute.QRILC internal error ("0
# (non-NA) cases") on a harder 40%-missing regime before ever reaching the negative-value bug,
# which is itself worth recording as a distinct failure mode below.
d <- make_dataset(n_features = 60, n_bio = 50, n_qc_per_batch = 0, n_batches = 1, seed = 5)
mat <- d$mat[d$class != "QC", , drop = FALSE]
mi <- inject_missingness(mat, d$true_abundance[1:60], n_mnar = 15, n_mar = 15, seed = 9)
mat_miss <- mi$mat
feat_mean <- colMeans(mat_miss, na.rm = TRUE)
feat_missrate <- colMeans(is.na(mat_miss))
abundance_rank <- rank(feat_mean) / ncol(mat_miss)
mnar_cols <- which(feat_missrate > 0.1 & abundance_rank < 0.35)  # == input 3's predicted_mnar, 17 features

cat(sprintf("Part A/B setup: %d diagnosed-MNAR features (input 3's exact repro subset)\n", length(mnar_cols)))

qrilc_in <- t(mat_miss[, mnar_cols, drop = FALSE])  # features in rows

## --- Part A: does the guard fire on the OLD (pre-fix) mistake? ---
cat("\n--- Part A: reproduce the pre-fix mistake (QRILC on RAW, non-log intensities) ---\n")
old_pattern_result <- tryCatch({
  qrilc_raw <- impute.QRILC(qrilc_in, tune.sigma = 1)[[1]]
  stopifnot(min(qrilc_raw, na.rm = TRUE) >= 0)   # the fixed SKILL.md's guard line, applied to the OLD call
  sprintf("guard did NOT fire; min imputed value = %.2f", min(qrilc_raw, na.rm = TRUE))
}, error = function(e) sprintf("guard FIRED: %s", conditionMessage(e)))
cat("Result:", old_pattern_result, "\n")

## --- Part B: the FIXED pattern, but on data with a few non-positive raw values (simulating
## upstream drift-correction fallout the Skill does not explicitly rule out) ---
cat("\n--- Part B: fixed log2/QRILC/2^x pattern, with 3 injected non-positive raw values ---\n")
qrilc_in_dirty <- qrilc_in
set.seed(79)
dirty_cells <- cbind(sample(seq_len(nrow(qrilc_in_dirty)), 3), sample(seq_len(ncol(qrilc_in_dirty)), 3))
# Only touch OBSERVED (non-NA) cells so this isn't just injecting more missingness.
for (i in seq_len(nrow(dirty_cells))) {
  r <- dirty_cells[i, 1]; cco <- dirty_cells[i, 2]
  if (!is.na(qrilc_in_dirty[r, cco])) qrilc_in_dirty[r, cco] <- c(0, -5.2, -0.001)[i]
}
n_nonpos <- sum(qrilc_in_dirty <= 0, na.rm = TRUE)
cat(sprintf("Injected %d non-positive observed values (simulating imperfect upstream correction)\n", n_nonpos))

log_mat <- suppressWarnings(log2(qrilc_in_dirty))
n_nan_from_log <- sum(is.nan(log_mat))
cat(sprintf("log2() produced %d NaN cell(s) from the non-positive inputs\n", n_nan_from_log))

qrilc_log_out <- tryCatch(impute.QRILC(log_mat, tune.sigma = 1)[[1]],
                            error = function(e) { cat("impute.QRILC errored:", conditionMessage(e), "\n"); NULL })

if (!is.null(qrilc_log_out)) {
  qrilc_out <- 2^qrilc_log_out
  n_nan_out <- sum(is.nan(qrilc_out))
  guard_b <- tryCatch({
    stopifnot(min(qrilc_out, na.rm = TRUE) >= 0)
    "PASS (guard did not fire)"
  }, error = function(e) sprintf("FIRED: %s", conditionMessage(e)))
  cat(sprintf("Post-imputation: %d NaN value(s) remain in qrilc_out. Guard verdict: %s\n", n_nan_out, guard_b))
  if (n_nan_out > 0 && guard_b == "PASS (guard did not fire)") {
    cat("FINDING: the documented stopifnot(min(...,na.rm=TRUE)>=0) guard uses na.rm=TRUE, which\n")
    cat("also strips NaN (is.na(NaN) is TRUE in R) -- so NaN values from log2() of a non-positive\n")
    cat("raw intensity pass the guard silently instead of being caught. The guard only catches\n")
    cat("the specific pre-fix failure mode (negative values), not this related one.\n")
  }
} else {
  cat("impute.QRILC could not run on the NaN-containing log matrix -- fails loudly, not silently.\n")
}
