library(limma)
library(ggplot2)
library(pheatmap)

# === 1. DATA IMPORT ===
# quote = '' / comment.char = '': MaxQuant text fields contain quotes and '#'; the defaults
# silently truncate the table with only an 'EOF within quoted string' warning. Check the count.
proteins <- read.delim('proteinGroups.txt', stringsAsFactors = FALSE, quote = '', comment.char = '')
stopifnot(nrow(proteins) == length(readLines('proteinGroups.txt')) - 1)
cat('Loaded', nrow(proteins), 'protein groups\n')

# Filter contaminants, reverse, only-by-site. Use %in%, NOT `!= '+'`: when a run flags none of a
# category the column is entirely empty, read.delim types it as logical NA, `NA != '+'` is NA, and
# subsetting by NA replaces every row with NAs while nrow() still looks right.
proteins <- proteins[!(proteins$Potential.contaminant %in% '+') &
                      !(proteins$Reverse %in% '+') &
                      !(proteins$Only.identified.by.site %in% '+'), ]
stopifnot(!all(is.na(proteins$Majority.protein.IDs)))
cat('After filtering:', nrow(proteins), 'proteins\n')

# Extract LFQ intensities
lfq_cols <- grep('^LFQ\\.intensity\\.', colnames(proteins), value = TRUE)
intensities <- proteins[, lfq_cols]
rownames(intensities) <- proteins$Majority.protein.IDs
colnames(intensities) <- gsub('LFQ\\.intensity\\.', '', colnames(intensities))

# === 2. LOG2 TRANSFORM, THEN INSPECT RAW DISTRIBUTIONS ===
intensities[intensities == 0] <- NA
log2_int <- log2(intensities)

# Inspect BEFORE normalizing (rule 4). Median-centering rescales every sample onto a common median,
# so it mathematically erases the 3x-low load that marks a failed injection -- after this point the
# failure is invisible. Identify and drop failures HERE.
# Inspect the RAW `Intensity.` columns, NOT `LFQ intensity`: MaxLFQ has ALREADY renormalized the LFQ
# columns onto a common scale, so a low load is largely gone from them before you ever look.
raw_cols <- grep('^Intensity\\.', colnames(proteins), value = TRUE)
raw_log2 <- log2(replace(proteins[, raw_cols], proteins[, raw_cols] == 0, NA))
colnames(raw_log2) <- gsub('^Intensity\\.', '', colnames(raw_log2))
raw_log2 <- raw_log2[, colnames(log2_int), drop = FALSE]
raw_median <- apply(raw_log2, 2, median, na.rm = TRUE)
id_counts <- colSums(!is.na(log2_int))
boxplot(raw_log2, las = 2, main = 'RAW log2 Intensity (pre-normalization)', ylab = 'log2 intensity')
print(data.frame(id_count = id_counts, raw_median_log2 = round(raw_median, 2),
                 load_shift_log2 = round(raw_median - median(raw_median), 2)))

# Flag on BOTH axes and as an OUTLIER, not a fixed fraction: a >=2x (1 log2) drop in raw median
# signal, OR an ID count more than 3 MADs below the cohort median. Each axis alone misses cases --
# a 3x-low injection loses its dimmest proteins entirely, so the SURVIVING median understates the
# deficit (a 3.0x low load can read as only -0.8 log2), while a 50%-of-median ID-count rule is so
# loose that a run at 82% of the median IDs, visibly low on both axes, passes it.
mad_ids <- mad(id_counts)
failed <- colnames(raw_log2)[(raw_median - median(raw_median)) <= -1 |
                             (mad_ids > 0 & id_counts < median(id_counts) - 3 * mad_ids)]
if (length(failed) > 0) {
    message('Dropping failed samples: ', paste(failed, collapse = ', '))
    log2_int <- log2_int[, !colnames(log2_int) %in% failed, drop = FALSE]
}

# === 3. NORMALIZE (only after the raw inspection above) ===
sample_medians <- apply(log2_int, 2, median, na.rm = TRUE)
global_median <- median(sample_medians)
normalized <- sweep(log2_int, 2, sample_medians - global_median)

# === 4. FILTER ON PER-GROUP COMPLETENESS (do NOT impute by default) ===
# Filter FIRST on completeness PER GROUP: keep a protein if it is valid in >= ~50-70%
# of replicates in AT LEAST ONE condition. A protein missing in every group fails QC.
sample_info <- read.csv('sample_annotation.csv')
# Re-align the annotation to the samples that SURVIVED the raw-distribution QC above; otherwise the
# column indexing below requests a dropped sample and errors (or silently misaligns the design).
sample_info <- sample_info[sample_info$sample %in% colnames(normalized), ]
sample_info$condition <- droplevels(factor(sample_info$condition))
min_frac <- 0.6   # >= 60% present within at least one group; tune 0.5-0.7 per design
group_complete <- sapply(levels(sample_info$condition), function(g) {
    cols <- sample_info$sample[sample_info$condition == g]
    rowSums(!is.na(normalized[, cols, drop = FALSE])) >= ceiling(length(cols) * min_frac)
})
valid_rows <- rowSums(group_complete) > 0
filtered <- normalized[valid_rows, ]
cat('Proteins after per-group completeness filter:', nrow(filtered), '\n')

# Missingness in label-free DDA is left-censored MNAR (missing BECAUSE low). The modern,
# correct approach is to MODEL the missingness in the likelihood, NOT impute it. See
# proteomics/differential-abundance for the decision (proDA / msqrob2 / MSstats-AFT).
# NOTHING BELOW IMPUTES: limma fits each protein on its OBSERVED values, so the completeness
# filter above is the only missing-value handling in the executed path.

# --- UPGRADE: model the dropout explicitly with proDA, then use `da` in place of `results` ---
# library(proDA)
# fit <- proDA(as.matrix(filtered), design = ~ condition, col_data = sample_info,
#              reference_level = 'Control')            # add batch: design = ~ batch + condition
# da <- test_diff(fit, contrast = 'conditionTreatment')   # columns: diff (log2FC), pval, adj_pval

# --- DO NOT: left-censored downshift imputation, then limma ---
# Downshift MANUFACTURES systematic false positives for on/off proteins near the detection limit
# (the volcano "anchor arms"): it pins missing values ~1.8 SD below the mean with an artificially
# tight 0.3 SD spread, inflating the t-numerator and deflating its denominator. The honest report
# for a protein fully missing in one group is "undetected in group B", NOT a fold change. If a
# reviewer demands a complete matrix anyway, seed it (set.seed) so the call list is reproducible,
# and report the on/off proteins separately -- see proteomics/differential-abundance.

# === 5. QC ===
# PCA needs a complete matrix; use the proteins observed everywhere rather than inventing values.
complete <- filtered[stats::complete.cases(filtered), , drop = FALSE]
cat('Proteins used for PCA (complete cases):', nrow(complete), '\n')
pca <- prcomp(t(complete), scale. = TRUE)
pca_df <- data.frame(PC1 = pca$x[, 1], PC2 = pca$x[, 2], Sample = rownames(pca$x))

# === 6. DIFFERENTIAL ANALYSIS (limma on the observed values) ===
# sample_info is already loaded and factored in step 4. Batch is a COVARIATE in the same model
# (rule 4); removeBatchEffect() is visualization-only, never an input to lmFit.
has_batch <- 'batch' %in% colnames(sample_info) && length(unique(sample_info$batch)) > 1
design <- if (has_batch) model.matrix(~ 0 + condition + factor(batch), data = sample_info) else
                         model.matrix(~ 0 + condition, data = sample_info)
colnames(design)[seq_along(levels(sample_info$condition))] <- levels(sample_info$condition)
colnames(design) <- make.names(colnames(design))
cat('design columns:', colnames(design), '| batch in design:', has_batch, '\n')

fit <- lmFit(as.matrix(filtered), design)
contrast <- makeContrasts(Treatment - Control, levels = design)
fit2 <- contrasts.fit(fit, contrast)

# Select on FDR ALONE. A post-hoc fold-change + significance double filter inflates FDR
# (a collider/selection effect; realized FDR can exceed 50%). To require a minimum effect,
# use the moderated minimum-fold-change test treat()/topTreat() instead of filtering after.
fit2_treat <- treat(fit2, lfc = log2(1.5), trend = TRUE, robust = TRUE)   # moderated min-FC test; trend+robust ~mandatory for label-free LFQ
results <- topTreat(fit2_treat, coef = 1, number = Inf)
results$protein <- rownames(results)
# A protein observed in only one group (or one batch level) has no estimable contrast: limma
# returns NA, and `adj.P.Val < 0.05` would make every downstream sum() NA. Report those separately
# as "undetected in group B" -- that is the honest statement, not a fold change.
results$significant <- !is.na(results$adj.P.Val) & results$adj.P.Val < 0.05

# === 7. OUTPUT ===
cat('\nResults:\n')
cat('  Contrast not estimable (report as undetected-in-group):', sum(is.na(results$logFC)), '\n')
cat('  Significant proteins:', sum(results$significant), '\n')
cat('  Up-regulated:', sum(results$significant & results$logFC > 0), '\n')
cat('  Down-regulated:', sum(results$significant & results$logFC < 0), '\n')

write.csv(results, 'proteomics_results.csv', row.names = FALSE)
