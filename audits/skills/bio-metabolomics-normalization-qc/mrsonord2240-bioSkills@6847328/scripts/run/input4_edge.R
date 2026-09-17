# Input 4 (Edge) -- Prompt:
# "My pilot batch only has 3 QC injections total (bracketing the ends). Can you drift-correct
# it with QC-RSC?" -- tests the Skill's own decision tree: "Sparse QCs (<5-6 spanning the
# batch) -> Coarse median-of-QC offset or no within-batch correction; LOESS/spline with too
# few QCs produces gaps/garbage." The correct behavior is to NOT force QCRSC past its own
# minQC guard, and to fall back to the documented coarse alternative.

source("F:/OpenScience/audits/bio-metabolomics-normalization-qc/data/make_synthetic.R")
library(pmp)

d <- make_dataset(n_features = 60, n_bio = 30, n_qc_per_batch = 3, n_batches = 1, seed = 21)
mat <- d$mat
fmat <- t(mat)  # features in rows, samples in columns (pmp convention)
classes <- d$class
batch_v <- d$batch
order_v <- d$order

cat(sprintf("Batch has %d QC injections (below the Skill's 5-6 QC sparse-data threshold)\n",
            sum(classes == "QC")))

# --- Attempt 1: call QCRSC honestly with minQC=5, THEN apply the fixed SKILL.md's documented
# guard line verbatim. Pre-fix, this all-NA failure was silent; post-fix the Skill tells the
# agent to check immediately and the guard should now stop execution loudly. ---
res <- QCRSC(df = fmat, order = order_v, batch = batch_v, classes = classes,
             spar = 0, log = TRUE, minQC = 5, qc_label = "QC")
out_mat <- if (methods::is(res, "SummarizedExperiment")) SummarizedExperiment::assay(res) else res
n_features_out <- nrow(out_mat)
n_all_na_features <- sum(apply(out_mat, 1, function(r) all(is.na(r))))
cat(sprintf("QCRSC did NOT refuse or error despite minQC=5 > 3 available QCs (still true post-fix,\n"))
cat(sprintf("  pmp's own behavior is unchanged; the fix adds a guard AROUND the call, not inside pmp).\n"))
cat(sprintf("  Returned %d features; %d of them are ALL-NA.\n", n_features_out, n_all_na_features))

guard_result <- tryCatch({
  stopifnot(any(rowSums(!is.na(out_mat)) > 0))
  "PASS (unexpected -- guard should have fired)"
}, error = function(e) sprintf("FIRED as intended: %s", conditionMessage(e)))
cat(sprintf("SKILL.md's documented guard line: %s\n", guard_result))

# --- Correct fallback per the Skill's decision tree: coarse median-of-QC offset, not a spline ---
coarse_correct <- function(fmat, is_qc) {
  qc_median <- apply(fmat[, is_qc, drop = FALSE], 1, median, na.rm = TRUE)
  offset <- qc_median / median(qc_median, na.rm = TRUE)  # per-feature scale, single flat offset
  fmat / offset
}
is_qc <- classes == "QC"
coarse <- coarse_correct(fmat, is_qc)
cat(sprintf("Coarse median-of-QC fallback applied instead (flat per-feature offset, no spline): %d features\n",
            nrow(coarse)))
cat("Correct decision: with only 3 QCs, do NOT fit a per-feature spline/LOESS vs order (Skill's\n")
cat("own failure mode: 'LOESS/spline with too few QCs produces gaps/garbage'); use the coarse\n")
cat("offset or skip within-batch correction and caveat the result instead.\n")
