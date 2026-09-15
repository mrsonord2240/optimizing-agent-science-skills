.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# Lead 2: what does normalizeBetweenArrays(method = 'scale') do to a LOG2 matrix?
# examples/limma_analysis.R line 22 calls it on log2 data under a "median centering" comment.
library(limma)
cat('limma', as.character(packageVersion('limma')), '\n')
set.seed(1)
m <- matrix(rnorm(2000 * 4, 20, 1), ncol = 4)
m[, 4] <- m[, 4] - 1.5                       # one sample loaded low: a pure additive shift on log2
colnames(m) <- paste0('S', 1:4)
sc <- normalizeBetweenArrays(m, method = 'scale')
med_center <- sweep(m, 2, apply(m, 2, median)) + median(apply(m, 2, median))
cat('\nColumn medians  raw   :', round(apply(m, 2, median), 3), '\n')
cat('Column medians  scale :', round(apply(sc, 2, median), 3), '\n')
cat('Column SD       raw   :', round(apply(m, 2, sd), 4), '\n')
cat('Column SD       scale :', round(apply(sc, 2, sd), 4), '\n')
cat('Column SD  med-center :', round(apply(med_center, 2, sd), 4), '\n')
ratio <- sc[, 4] / m[, 4]
cat('\nS4 scale/raw ratio (constant => multiplicative):', round(range(ratio), 6), '\n')
diffs <- sc[, 4] - m[, 4]
cat('S4 scale - raw (constant => additive):', round(range(diffs), 4), '\n')
# consequence: a protein 4 log2 units above the median in S4 vs S1
hi <- which.max(m[, 4]); lo <- which.min(m[, 4])
cat('\nHighest-S4 protein: raw S4 - median(S4) =', round(m[hi, 4] - median(m[, 4]), 3),
    '| after scale =', round(sc[hi, 4] - median(sc[, 4]), 3), '\n')
cat('Lowest-S4 protein : raw S4 - median(S4) =', round(m[lo, 4] - median(m[, 4]), 3),
    '| after scale =', round(sc[lo, 4] - median(sc[, 4]), 3), '\n')
# A null protein at a given abundance: S4 residual vs other samples after each method
x <- rep(24, 4); x[4] <- 24 - 1.5            # null protein 4 log2 above typical median, S4 loaded low
mm <- cbind(m, NA); # not used
f <- apply(m, 2, median); target <- exp(mean(log(f)))
cat('Null protein at log2 24 (S4 raw 22.5): after scale S4 =', round(22.5 * target / f[4], 3),
    'vs other samples ~', round(24 * target / f[1], 3), '\n')
cat('\nSource of normalizeMedianValues (what method="scale" calls):\n')
print(body(limma::normalizeMedianValues))
