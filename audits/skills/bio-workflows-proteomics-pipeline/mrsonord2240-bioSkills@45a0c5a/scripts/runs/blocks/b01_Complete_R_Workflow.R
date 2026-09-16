library(limma)
library(ggplot2)
library(pheatmap)

# === 1. DATA IMPORT ===
proteins <- read.delim('proteinGroups.txt', stringsAsFactors = FALSE)
cat('Loaded', nrow(proteins), 'protein groups\n')

# Filter contaminants, reverse, only-by-site
proteins <- proteins[proteins$Potential.contaminant != '+' &
                      proteins$Reverse != '+' &
                      proteins$Only.identified.by.site != '+', ]
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
boxplot(log2_int, las = 2, main = 'RAW log2 LFQ (pre-normalization)', ylab = 'log2 intensity')
id_counts <- colSums(!is.na(log2_int))
print(data.frame(id_count = id_counts, raw_median_log2 = round(apply(log2_int, 2, median, na.rm = TRUE), 2)))

# <50% of the cohort median ID count is a failed injection / low load, not biology.
failed <- names(id_counts)[id_counts < 0.5 * median(id_counts)]
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
# proteomics/differential-abundance for the decision (proDA / msqrob2 / MSstats-AFT). The
# proDA path below is the RECOMMENDED route; the impute-then-limma path is a fallback.

# --- RECOMMENDED: model the missingness with proDA (no imputation) ---
# library(proDA)
# fit <- proDA(as.matrix(filtered), design = ~ condition, col_data = sample_info,
#              reference_level = 'Control')
# da <- test_diff(fit, contrast = 'conditionTreatment')   # columns: diff (log2FC), pval, adj_pval
# (Skip the === 5-6 impute/limma blocks below when using proDA.)

# --- FALLBACK ONLY: left-censored downshift imputation, then limma ---
# WARNING: downshift MANUFACTURES systematic false positives for on/off proteins near the
# detection limit (the volcano "anchor arms"): it pins missing values ~1.8 SD below the mean
# with an artificially tight 0.3 SD spread, inflating the t-statistic. The honest report for
# a protein fully missing in one group is "undetected in group B", NOT a fold change.
impute_minprob <- function(x) {
    nas <- is.na(x)
    if (all(nas)) return(x)
    x[nas] <- rnorm(sum(nas), mean = mean(x, na.rm = TRUE) - 1.8 * sd(x, na.rm = TRUE),
                    sd = 0.3 * sd(x, na.rm = TRUE))
    x
}
imputed <- as.data.frame(t(apply(filtered, 1, impute_minprob)))

# === 5. QC ===
# PCA
pca <- prcomp(t(imputed), scale. = TRUE)
pca_df <- data.frame(PC1 = pca$x[, 1], PC2 = pca$x[, 2], Sample = rownames(pca$x))

# === 6. DIFFERENTIAL ANALYSIS (fallback impute-then-limma path) ===
# sample_info is already loaded and factored in step 4. Put any batch in the design
# (~ batch + condition); removeBatchEffect() is visualization-only, never an input to lmFit.
design <- model.matrix(~ 0 + condition, data = sample_info)
colnames(design) <- levels(sample_info$condition)

fit <- lmFit(as.matrix(imputed), design)
contrast <- makeContrasts(Treatment - Control, levels = design)
fit2 <- contrasts.fit(fit, contrast)

# Select on FDR ALONE. A post-hoc fold-change + significance double filter inflates FDR
# (a collider/selection effect; realized FDR can exceed 50%). To require a minimum effect,
# use the moderated minimum-fold-change test treat()/topTreat() instead of filtering after.
fit2_treat <- treat(fit2, lfc = log2(1.5), trend = TRUE, robust = TRUE)   # moderated min-FC test; trend+robust ~mandatory for label-free LFQ
results <- topTreat(fit2_treat, coef = 1, number = Inf)
results$protein <- rownames(results)
results$significant <- results$adj.P.Val < 0.05

# === 7. OUTPUT ===
cat('\nResults:\n')
cat('  Significant proteins:', sum(results$significant), '\n')
cat('  Up-regulated:', sum(results$significant & results$logFC > 0), '\n')
cat('  Down-regulated:', sum(results$significant & results$logFC < 0), '\n')

write.csv(results, 'proteomics_results.csv', row.names = FALSE)
