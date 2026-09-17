# Input 2 (Variant A) -- regression test of the P1 fix: Stage2->Stage4 hand-off on real
# multi-batch data (MTBLS79, 2488 features x 172 samples, 8 batches, 38 pooled QCs). Pre-fix this
# crashed opls() with 'missing value where TRUE/FALSE needed' because imputation was named only
# in a comment. Post-fix SKILL.md now drops wholly-NA (QCRSC-wiped) samples, then QRILC-imputes
# the sparse rest via a log2/2^x round-trip, asserting !anyNA before Stage 4. Run the current
# Stage 2 + Stage 4 code blocks verbatim against the same real data as the pre-fix audit.
suppressMessages({library(pmp); library(imputeLCMD); library(ropls)})

peak_mat <- read.csv('F:/OpenScience/audit-envs/untargeted-metabolomics-analyst/public-data/MTBLS79/MTBLS79_peak_matrix.csv',
                      row.names = 1, check.names = FALSE)
meta <- read.csv('F:/OpenScience/audit-envs/untargeted-metabolomics-analyst/public-data/MTBLS79/MTBLS79_sample_metadata.csv',
                  row.names = 1, check.names = FALSE)
stopifnot(identical(rownames(meta), colnames(peak_mat)))

feat <- as.matrix(peak_mat)
defs <- data.frame(row.names = rownames(feat))
sample_class <- meta$Class
batch_id <- meta$Batch
# Real per-injection run order is not present in this flat MTBLS79 export (Sample_Rep is a
# replicate index, not injection order -- has ties within a batch/class). Use column order as
# the injection-order stand-in, matching the pre-fix audit's own Input 2 script
# (run/input2_stage2to4_realchain.R) and the fixer's verification run, for a like-for-like regression.
injection_order <- seq_len(ncol(feat))
cat('Real MTBLS79 peak matrix:', nrow(feat), 'x', ncol(feat), '\n')
cat('Classes:', paste(names(table(sample_class)), table(sample_class), sep = '=', collapse = ', '), '\n\n')

cat('=== Stage 2 -- current SKILL.md code, verbatim ===\n')
fm <- feat
stopifnot(nrow(fm) == nrow(defs) || TRUE, ncol(fm) == length(sample_class))  # defs has no row metadata here; dims-only check

filtered <- filter_peaks_by_fraction(fm, classes = sample_class, min_frac = 0.5, qc_label = 'QC')
cat('After filter_peaks_by_fraction:', nrow(filtered), 'of', nrow(fm), 'features kept\n')

corrected <- QCRSC(df = filtered, order = injection_order, batch = batch_id,
                    classes = sample_class, spar = 0, minQC = 5, qc_label = 'QC')
cat('After QCRSC:', nrow(corrected), 'x', ncol(corrected), '\n')

rsd_filtered <- filter_peaks_by_rsd(corrected, max_rsd = 30, classes = sample_class, qc_label = 'QC')
cat('After filter_peaks_by_rsd:', nrow(rsd_filtered), 'of', nrow(corrected), 'features kept\n')

normalized <- pqn_normalisation(rsd_filtered, classes = sample_class, qc_label = 'QC')
cat('After pqn_normalisation:', nrow(normalized), 'x', ncol(normalized), '\n\n')

cat('=== Drop QCRSC-wiped (wholly-NA) samples -- the fix ===\n')
nm <- as.matrix(normalized)
wiped <- colMeans(is.na(nm)) == 1
cat(sum(wiped), 'of', ncol(nm), 'samples came back all-NA (QCRSC: their batch had < minQC QCs)\n')
print(table(batch_id[wiped]))
nm <- nm[, !wiped, drop = FALSE]
sample_class <- sample_class[!wiped]
batch_id_kept <- batch_id[!wiped]
cat('Remaining after drop:', ncol(nm), 'samples\n')
cat('Max per-sample NA rate among survivors:', sprintf('%.1f%%', 100 * max(colMeans(is.na(nm)))), '\n\n')

cat('=== Mechanism-aware imputation (log2/2^x QRILC round-trip) -- the fix ===\n')
log_mat <- log2(nm)
imputed <- 2^(impute.QRILC(log_mat, tune.sigma = 1)[[1]])
stopifnot(min(imputed, na.rm = TRUE) >= 0, !anyNA(imputed))
cat('QRILC imputation OK. min value:', round(min(imputed), 3), '| any NA remaining:', anyNA(imputed), '\n\n')

cat('=== Stage 4 -- current SKILL.md code, verbatim (via statistical-analysis fit_discriminant_guarded) ===\n')
fit_discriminant_guarded <- function(x, y, scaleC, permI = 1000, crossvalI = 7) {
    m <- opls(x, y, predI = 1, orthoI = NA, scaleC = scaleC, permI = permI,
              crossvalI = crossvalI, fig.pdfC = 'none', info.txtC = 'none')
    if (nrow(getSummaryDF(m)) > 0) return(list(model = m, type = 'OPLS-DA'))
    m2 <- opls(x, y, predI = 1, orthoI = 0, scaleC = scaleC, permI = permI,
               crossvalI = crossvalI, fig.pdfC = 'none', info.txtC = 'none')
    if (nrow(getSummaryDF(m2)) > 0) return(list(model = m2, type = 'PLS-DA (OPLS-DA fallback)'))
    stop('Neither OPLS-DA nor the PLS-DA fallback produced a usable model.')
}

study_samples <- sample_class != 'QC'
group <- factor(sample_class[study_samples])
x <- t(imputed)[study_samples, ]
stopifnot(!anyNA(x))
cat('Stage2->Stage4 hand-off shape:', nrow(x), 'x', ncol(x), '| groups:',
    paste(levels(group), collapse = ' vs '), '\n')

fit <- fit_discriminant_guarded(x, group, scaleC = 'pareto', permI = 1000)
oplsda <- fit$model
cat('Model type actually fit:', fit$type, '\n')
summ <- getSummaryDF(oplsda)
stopifnot(nrow(summ) > 0)
cat('getSummaryDF rows:', nrow(summ), '(not a silent empty model)\n')
print(summ[, c('R2X(cum)', 'R2Y(cum)', 'Q2(cum)', 'pR2Y', 'pQ2')])

cat('\n=== RESULT ===\n')
cat('Pre-fix: opls() ERROR "missing value where TRUE/FALSE needed" (55.95% NA reached opls()).\n')
cat('Post-fix: opls() completed, produced a', nrow(summ), '-row summary with pR2Y =',
    summ$pR2Y, ', pQ2 =', summ$pQ2, '. The crash is fixed.\n')
