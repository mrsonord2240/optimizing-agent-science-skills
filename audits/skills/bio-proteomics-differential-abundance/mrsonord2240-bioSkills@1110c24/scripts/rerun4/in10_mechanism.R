# NEW Input 10, part 2: the offset sweep showed a UNIFORM -0.20 offset causes 0
# false positives, while real per-run median normalization at the same median
# offset causes 31. So the median offset cannot be the mechanism. This measures
# what actually differs: the SPREAD of the per-protein shift.
suppressPackageStartupMessages({library(QFeatures); library(msqrob2); library(MsCoreUtils)})
DD <- 'F:/OpenScience/audits/bio-proteomics-differential-abundance/data'
DW <- 'F:/OpenScience/audits/bio-proteomics-differential-abundance/rerun4'

ann <- read.csv(file.path(DD, 'annotation_msstats.csv'), stringsAsFactors = FALSE)
ev <- read.table(file.path(DD, 'evidence.txt'), sep = '\t', header = TRUE, quote = '', comment.char = '')
ev <- ev[!(ev$Reverse %in% '+') & !(ev$Potential.contaminant %in% '+') &
           !is.na(ev$Intensity) & ev$Intensity > 0, ]
ev$feature <- paste(ev$Modified.sequence, ev$Charge, sep = '_')
runs <- as.character(ann$Raw.file)
agg <- aggregate(Intensity ~ feature + Raw.file + Leading.razor.protein, data = ev, FUN = sum)
wide <- reshape(agg, idvar = c('feature', 'Leading.razor.protein'), timevar = 'Raw.file', direction = 'wide')
colnames(wide) <- sub('Intensity.', '', colnames(wide), fixed = TRUE)
wide <- wide[, c('feature', 'Leading.razor.protein', runs)]
names(wide)[2] <- 'protein'
trt <- ann$Condition == 'Treatment'

L0 <- log2(as.matrix(wide[, runs]))
med <- apply(L0, 2, median, na.rm = TRUE)
Lall <- sweep(L0, 2, med) + median(med)                 # per-run median over ALL detected peptides
Lunif <- L0; Lunif[, trt] <- Lunif[, trt] - 0.20        # uniform -0.20 into Treatment

cat('per-run median shifts applied by center.median (log2):\n  ',
    paste(sprintf('%+.3f', med - median(med)), collapse = ' '), '\n')
cat('  mean shift Control', sprintf('%+.3f', mean((med - median(med))[!trt])),
    '| Treatment', sprintf('%+.3f', mean((med - median(med))[trt])),
    '| difference', sprintf('%+.3f', mean((med - median(med))[trt]) - mean((med - median(med))[!trt])), '\n')

# per-PROTEIN change in log2FC caused by each transformation
prot_fc <- function(L) {
  fc <- rowMeans(L[, trt, drop = FALSE], na.rm = TRUE) - rowMeans(L[, !trt, drop = FALSE], na.rm = TRUE)
  tapply(fc, wide$protein, mean, na.rm = TRUE)
}
d_all <- prot_fc(Lall) - prot_fc(L0)
d_unif <- prot_fc(Lunif) - prot_fc(L0)
q <- function(x) sprintf('median %+.3f | sd %.3f | IQR %.3f | range %+.3f..%+.3f',
                         median(x, na.rm = TRUE), sd(x, na.rm = TRUE),
                         IQR(x, na.rm = TRUE), min(x, na.rm = TRUE), max(x, na.rm = TRUE))
cat('\nper-protein shift in log2FC:\n')
cat('  center.median over all peptides :', q(d_all), '\n')
cat('  uniform -0.20 into Treatment    :', q(d_unif), '\n')
cat('\n  -> the two have the SAME median. If the median offset were the mechanism,\n',
    '     they would produce the same false-positive count. They do not.\n')
cat('  proteins whose shift differs from the median by > 0.10 log2:',
    sum(abs(d_all - median(d_all, na.rm = TRUE)) > 0.10, na.rm = TRUE), '(center.median) vs',
    sum(abs(d_unif - median(d_unif, na.rm = TRUE)) > 0.10, na.rm = TRUE), '(uniform)\n')

# is the heterogeneity driven by detection composition, as the Skill says?
n_obs <- tapply(rowSums(!is.na(L0)), wide$protein, mean)
cc <- tapply(as.integer(stats::complete.cases(L0)), wide$protein, mean)
ok <- is.finite(d_all) & is.finite(n_obs)
cat('\n  corr(|per-protein shift - median|, mean peptide completeness):',
    round(cor(abs(d_all[ok] - median(d_all, na.rm = TRUE)), cc[ok], use = 'complete.obs'), 3), '\n')
cat('  corr(|per-protein shift - median|, mean peptides observed per run):',
    round(cor(abs(d_all[ok] - median(d_all, na.rm = TRUE)), n_obs[ok], use = 'complete.obs'), 3), '\n')
