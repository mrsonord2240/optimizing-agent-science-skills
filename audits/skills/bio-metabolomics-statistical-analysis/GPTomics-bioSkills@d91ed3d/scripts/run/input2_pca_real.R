# Audit input 2 (Variant A) -- bio-metabolomics-statistical-analysis
# User request: "I have a real MTBLS79 LC-MS peak matrix (66 control / 68 case /
# 38 pooled-QC samples across 8 batches). Run PCA with Pareto scaling and check
# whether the QC samples cluster tightly before I trust anything downstream."
#
# Real public data (MTBLS79), not synthetic. Upstream normalization/imputation
# is out of this Skill's scope (metabolomics/normalization-qc); a per-feature
# median imputation is applied here only as a minimal stand-in so PCA can run,
# and is called out as such rather than presented as part of this Skill's job.
library(ropls)

data_dir <- 'F:/OpenScience/audit-envs/untargeted-metabolomics-analyst/public-data/MTBLS79'
peak <- read.csv(file.path(data_dir, 'MTBLS79_peak_matrix.csv'),
                  row.names = 1, check.names = FALSE)
meta <- read.csv(file.path(data_dir, 'MTBLS79_sample_metadata.csv'),
                  row.names = 1, check.names = FALSE)
meta <- meta[colnames(peak), ]
stopifnot(all(rownames(meta) == colnames(peak)))

cat('Loaded real MTBLS79 peak matrix:', nrow(peak), 'features x', ncol(peak), 'samples\n')
cat('Class counts:', paste(names(table(meta$Class)), table(meta$Class), sep = '=', collapse = ', '), '\n')

# Minimal per-feature median imputation (stand-in for upstream normalization-qc step)
mat <- as.matrix(peak)
n_na <- sum(is.na(mat))
for (i in seq_len(nrow(mat))) {
    row_na <- is.na(mat[i, ])
    if (any(row_na)) mat[i, row_na] <- median(mat[i, !row_na], na.rm = TRUE)
}
cat('Imputed', n_na, 'missing values by per-feature median (stand-in only, not this Skill\'s step)\n')

# Log2 transform (heteroscedastic MS intensities) then PCA with explicit Pareto scaling
logmat <- log2(mat)
pca <- opls(t(logmat), scaleC = 'pareto', fig.pdfC = 'none', info.txtC = 'none')
scores <- getScoreMN(pca)
summ <- getSummaryDF(pca)
cat('\nR2X(cum) by component:\n')
print(summ)

# QC clustering check: distance of QC sample scores from the QC centroid vs.
# distance of non-QC (C/S) sample scores from the overall centroid, in PC1-PC2 space
is_qc <- meta$Class == 'QC'
qc_scores <- scores[is_qc, 1:2]
other_scores <- scores[!is_qc, 1:2]
qc_centroid <- colMeans(qc_scores)
qc_dispersion <- mean(sqrt(rowSums((sweep(qc_scores, 2, qc_centroid))^2)))
other_centroid <- colMeans(other_scores)
other_dispersion <- mean(sqrt(rowSums((sweep(other_scores, 2, other_centroid))^2)))
cat(sprintf('\nMean QC distance from QC centroid (PC1-PC2): %.2f\n', qc_dispersion))
cat(sprintf('Mean non-QC distance from non-QC centroid (PC1-PC2): %.2f\n', other_dispersion))
cat(sprintf('QC tighter than biological samples: %s (ratio %.2f)\n',
            qc_dispersion < other_dispersion, qc_dispersion / other_dispersion))

# Hotelling T2 outlier check via ropls's own diagnostic
cat('\nSample outlier flags (Hotelling T2 / DModX), first 10 rows:\n')
print(head(pca@suppLs$outlierDF, 10))
