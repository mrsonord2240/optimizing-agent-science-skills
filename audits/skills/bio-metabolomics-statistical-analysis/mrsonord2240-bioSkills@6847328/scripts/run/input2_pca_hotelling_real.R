# Regression test for pre-fix P1 finding: "Hotelling T2 / PCA outlier check named but never
# demonstrated with code." The fix added a runnable Hotelling T2 snippet to SKILL.md's PCA
# section (ropls exposes no ready accessor; compute it directly from getScoreMN()). Re-run
# that snippet verbatim on the same real MTBLS79 data used pre-fix, plus a synthetic check
# with two planted outliers to confirm the snippet actually flags outliers when present
# (the real data alone can't prove that -- 0 flagged could mean "works" or "broken").
library(ropls)

cat('=== Part A: real MTBLS79 data (same data + imputation as the pre-fix audit) ===\n')
meta <- read.csv('F:/OpenScience/audit-envs/untargeted-metabolomics-analyst/public-data/MTBLS79/MTBLS79_sample_metadata.csv', row.names = 1)
peaks <- read.csv('F:/OpenScience/audit-envs/untargeted-metabolomics-analyst/public-data/MTBLS79/MTBLS79_peak_matrix.csv', row.names = 1, check.names = FALSE)
cat('Loaded real MTBLS79 peak matrix:', nrow(peaks), 'features x', ncol(peaks), 'samples\n')
feature_matrix <- t(as.matrix(peaks))  # samples x features, per SKILL.md's `t(feature_matrix)` call

n_na <- sum(is.na(feature_matrix))
# per-feature median imputation -- explicit stand-in for the out-of-scope normalization-qc step,
# same disclosed workaround used pre-fix (SKILL.md points to metabolomics/normalization-qc for this)
for (j in seq_len(ncol(feature_matrix))) {
    col <- feature_matrix[, j]
    if (any(is.na(col))) feature_matrix[is.na(col), j] <- median(col, na.rm = TRUE)
}
cat('Imputed', n_na, 'missing values by per-feature median (stand-in only, not this Skill\'s own step)\n')

pca <- opls(feature_matrix, scaleC = 'pareto', fig.pdfC = 'none', info.txtC = 'none')
scores <- getScoreMN(pca)
cat('R2X(cum):\n'); print(getSummaryDF(pca)[, 'R2X(cum)', drop = FALSE])

# --- Hotelling T2 snippet from SKILL.md, copied verbatim ---
A <- ncol(scores); N <- nrow(scores)
lambda <- apply(scores, 2, function(col) sum(col^2) / (N - 1))
t2 <- rowSums(sweep(scores^2, 2, lambda, '/'))
t2_crit95 <- A * (N - 1) / (N - A) * qf(0.95, A, N - A)
outliers <- rownames(scores)[t2 > t2_crit95]
cat(sprintf('N samples=%d, A components=%d, T2 crit (95%%)=%.2f\n', N, A, t2_crit95))
cat('Outliers flagged on real data:', length(outliers), 'of', N, '\n')
if (length(outliers) > 0) print(outliers)

cat('\n=== Part B: synthetic data with 2 planted outliers (proves the snippet actually detects something) ===\n')
set.seed(7)
n <- 60; p <- 200
X <- matrix(rnorm(n * p, mean = 10, sd = 1), nrow = n, ncol = p)
rownames(X) <- paste0('S', seq_len(n)); colnames(X) <- paste0('M', seq_len(p))
X[1, ] <- X[1, ] + 15   # planted outlier 1: large uniform shift
X[2, seq_len(50)] <- X[2, seq_len(50)] + 20  # planted outlier 2: shift in a feature subset

pca2 <- opls(X, scaleC = 'pareto', fig.pdfC = 'none', info.txtC = 'none')
scores2 <- getScoreMN(pca2)
A2 <- ncol(scores2); N2 <- nrow(scores2)
lambda2 <- apply(scores2, 2, function(col) sum(col^2) / (N2 - 1))
t2_2 <- rowSums(sweep(scores2^2, 2, lambda2, '/'))
t2_crit95_2 <- A2 * (N2 - 1) / (N2 - A2) * qf(0.95, A2, N2 - A2)
cat(sprintf('T2 crit (95%%)=%.2f\n', t2_crit95_2))
cat('T2 for planted outlier S1:', round(t2_2['S1'], 2), '\n')
cat('T2 for planted outlier S2:', round(t2_2['S2'], 2), '\n')
cat('T2 range for the other 58 (non-outlier) samples:', round(range(t2_2[!(rownames(scores2) %in% c('S1','S2'))]), 3), '\n')
flagged <- names(t2_2)[t2_2 > t2_crit95_2]
cat('Flagged as outliers:', paste(flagged, collapse = ', '), '\n')
cat('Both planted outliers correctly flagged:', all(c('S1','S2') %in% flagged), '\n')
cat('No non-planted sample incorrectly flagged:', !any(setdiff(flagged, c('S1','S2')) %in% rownames(scores2)) || length(setdiff(flagged, c('S1','S2'))) == 0, '\n')
