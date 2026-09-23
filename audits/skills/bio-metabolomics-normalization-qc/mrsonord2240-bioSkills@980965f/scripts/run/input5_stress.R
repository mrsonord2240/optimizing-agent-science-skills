# Input 5 (Stress / multi-part) -- Prompt:
# "Run the full pipeline on my 3-batch study: filter junk features, drift-correct, batch-align,
# impute, and normalize. Also -- my case/control assignment happens to line up with which batch
# each animal was run in, is that a problem?"
# Synthetic data (this audit): group is DELIBERATELY 100% confounded with batch (half the
# batches are all-control, half all-case) -- the Skill's own "information-theoretically
# unwinnable" scenario. Correct behavior: run the mechanical steps, but flag the confound loudly
# rather than silently reporting group-corrected results as trustworthy.

source("F:/OpenScience/audits/bio-metabolomics-normalization-qc/data/make_synthetic.R")
library(pmp)
library(matrixStats)

d <- make_dataset(n_features = 80, n_bio = 60, n_qc_per_batch = 6, n_batches = 4,
                   confound_group_with_batch = TRUE, seed = 33)
fmat <- t(d$mat)
classes <- d$class
batch_v <- d$batch
order_v <- d$order
group_v <- d$group

# --- Confound check FIRST, before running anything else (this is the correctness-critical step) ---
bio_idx <- which(classes != "QC")
tab <- table(batch = batch_v[bio_idx], group = group_v[bio_idx])
cat("Batch x group cross-tab (biological samples only):\n"); print(tab)
chi <- suppressWarnings(chisq.test(tab))
cat(sprintf("\nAssociation strength (Cramer's V-style check): p=%.2g; batches are %s with group.\n",
            chi$p.value,
            if (all(rowSums(tab > 0) == 1)) "PERFECTLY CONFOUNDED (each batch is single-group)" else "not fully confounded"))

# --- 1. Detection-rate filter ---
detect_rate <- rowMeans(!is.na(fmat))
fmat_f <- fmat[detect_rate >= 0.5, , drop = FALSE]
cat(sprintf("\nAfter detection-rate filter: %d / %d features\n", nrow(fmat_f), nrow(fmat)))

# --- 2. Within-batch drift correction (mechanically fine; batch confound doesn't block this step) ---
corrected <- tryCatch(
  QCRSC(df = fmat_f, order = order_v, batch = batch_v, classes = classes,
        spar = 0, log = TRUE, minQC = 4, qc_label = "QC"),
  error = function(e) { cat("QCRSC error:", conditionMessage(e), "\n"); NULL })
mat_c <- if (!is.null(corrected)) {
  if (methods::is(corrected, "SummarizedExperiment")) SummarizedExperiment::assay(corrected) else corrected
} else fmat_f
if (!is.null(corrected)) {
  stopifnot(any(rowSums(!is.na(mat_c)) > 0))  # fixed SKILL.md's documented QCRSC guard
  cat("QCRSC all-NA guard: PASS\n")
}
cat(sprintf("After drift correction: %d features (NA rows: %d)\n",
            nrow(mat_c), sum(apply(mat_c, 1, function(r) all(is.na(r))))))

# --- 3. Between-batch alignment: QC-anchored, NOT ComBat (ComBat here would be fitting group
# effect out of existence, since group ~ batch perfectly -- exactly the Nygaard 2016 trap) ---
qc_cols <- which(classes == "QC")
batch_offsets <- sapply(sort(unique(batch_v)), function(b) {
  cols_b <- qc_cols[batch_v[qc_cols] == b]
  rowMedians(mat_c[, cols_b, drop = FALSE], na.rm = TRUE)
})
colnames(batch_offsets) <- as.character(sort(unique(batch_v)))
grand_ref <- rowMedians(mat_c[, qc_cols, drop = FALSE], na.rm = TRUE)
mat_aligned <- mat_c
for (b in sort(unique(batch_v))) {
  cols_b <- which(batch_v == b)
  scale_b <- grand_ref / batch_offsets[, as.character(b)]
  scale_b[!is.finite(scale_b)] <- 1
  mat_aligned[, cols_b] <- mat_c[, cols_b] * scale_b
}
cat("QC-anchored batch alignment applied (ComBat explicitly NOT used: group is collinear with\n")
cat("batch, so ComBat's empirical-Bayes shrinkage cannot distinguish batch step-change from the\n")
cat("case/control effect -- it would either fabricate or delete the effect, per Nygaard 2016).\n")

cat("\n*** DESIGN FLAG: case/control status is perfectly confounded with batch in this dataset.\n")
cat("*** No correction algorithm (QC-anchored or ComBat) can separate 'batch' from 'group' here.\n")
cat("*** Any downstream group difference is equally explainable by an uncorrected batch artifact.\n")
cat("*** This must be reported as a design limitation, not resolved by normalization.\n")
