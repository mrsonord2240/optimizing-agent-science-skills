# Input 1 (Canonical) -- regression test of the pre-fix Stage1->Stage2 orientation bug.
# Pre-fix SKILL.md: `fm <- t(feat)`, captioned "features in ROWS, samples in COLUMNS", which
# actually inverted a features-in-rows featureValues() output. Post-fix SKILL.md (current):
#   fm <- feat
#   stopifnot(nrow(fm) == nrow(defs), ncol(fm) == length(sample_class))
# Re-run against the SAME real xcms output used in the pre-fix audit (574 real faahKO features x
# 12 samples, reused from bio-metabolomics-xcms-preprocessing's run/feature_table_input1.csv).
suppressMessages(library(pmp))

feat_csv <- read.csv('F:/OpenScience/audits/bio-metabolomics-xcms-preprocessing/run/feature_table_input1.csv',
                      row.names = 1, check.names = FALSE)
feat <- as.matrix(feat_csv[, -(1:2)])  # drop mz, rt columns -> features x samples
mode(feat) <- 'numeric'
defs <- data.frame(mzmed = feat_csv$mz, rtmed = feat_csv$rt, row.names = rownames(feat_csv))
sample_class <- rep(c('KO', 'WT'), each = 6)

cat('Real xcms featureValues()-shaped input:', nrow(feat), 'x', ncol(feat), '\n\n')

cat('=== Current SKILL.md Stage 2 hand-off code, verbatim ===\n')
fm <- feat
ok <- tryCatch({
  stopifnot(nrow(fm) == nrow(defs), ncol(fm) == length(sample_class))
  TRUE
}, error = function(e) { cat('stopifnot FAILED:', conditionMessage(e), '\n'); FALSE })
cat('No transpose applied. dim(fm) =', nrow(fm), 'x', ncol(fm), '| dim(defs) =', nrow(defs),
    '| length(sample_class) =', length(sample_class), '\n')
cat('stopifnot dimension check:', if (ok) 'PASSED' else 'FAILED', '\n\n')

cat('=== Feed fm into the documented pmp call ===\n')
# faahKO has no pooled-QC class; use KO as the qc_label reference group, matching the pre-fix
# audit's own Input 1 script (run/input1_glue_orientation.R) for a like-for-like regression.
res <- filter_peaks_by_fraction(fm, classes = sample_class, min_frac = 0.5, qc_label = 'KO')
cat('filter_peaks_by_fraction(fm) result:', nrow(res), 'of', nrow(fm), 'features kept, dim',
    nrow(res), 'x', ncol(res), '\n\n')

cat('=== Regression check vs pre-fix bug: is fm still features-in-rows? ===\n')
cat('fm rows == feat rows (features):', nrow(fm) == nrow(feat), '\n')
cat('fm cols == feat cols (samples):', ncol(fm) == ncol(feat), '\n')
if (nrow(fm) == nrow(feat) && ncol(fm) == ncol(feat)) {
  cat('PASS: orientation preserved, no inversion. The pre-fix `t(feat)` bug is gone.\n')
} else {
  cat('FAIL: orientation still wrong.\n')
}
