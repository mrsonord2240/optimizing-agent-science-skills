# Batch-design Input 7 (NEW, targets the P1 fix's own caveat): the fixed SKILL.md's SVA block
# says restricting to complete-observation features "biases the surrogate variables toward
# abundant, well-detected features". Fact-check that claim on the SAME real synthetic MaxQuant
# matrix used in Input 4, rather than accepting the fixer's stated rationale on faith: is the
# 738-feature complete-case subset actually higher-abundance / better-detected than the 762
# features it drops?
.libPaths(c('F:/OpenScience/audit-envs/untargeted-metabolomics-analyst/R-lib', .libPaths()))
BB <- 'F:/OpenScience/audits/bio-experimental-design-batch-design'
pg <- read.delim(file.path(BB, 'data', 'proteinGroups.txt'), quote = '', check.names = FALSE)
pg <- pg[pg$Reverse != '+' & pg$`Potential contaminant` != '+' & pg$`Only identified by site` != '+', ]
M <- as.matrix(pg[, grep('^LFQ intensity ', names(pg))]); M[M == 0] <- NA; M <- log2(M)

complete_idx <- stats::complete.cases(M)
cat(sprintf('complete features: %d | incomplete (dropped) features: %d\n', sum(complete_idx), sum(!complete_idx)))

mean_abund_complete   <- rowMeans(M[complete_idx, , drop = FALSE], na.rm = TRUE)
mean_abund_incomplete <- rowMeans(M[!complete_idx, , drop = FALSE], na.rm = TRUE)
n_detected_complete   <- rowSums(!is.na(M[complete_idx, , drop = FALSE]))
n_detected_incomplete <- rowSums(!is.na(M[!complete_idx, , drop = FALSE]))

# Some "incomplete" features are undetected in ALL 8 samples (0/8) -- rowMeans(na.rm=TRUE) on an
# all-NA row is NaN by definition (not a bug in the Skill's logic, a property of this real-style
# MaxQuant export). Report how many, and use na.rm=TRUE on the aggregate so they don't blank the
# whole comparison; also report the comparison restricted to features detected in >=1 sample.
n_fully_undetected <- sum(is.nan(mean_abund_incomplete))
cat(sprintf('dropped features with 0/8 detections (LFQ intensity entirely absent): %d/%d\n',
            n_fully_undetected, length(mean_abund_incomplete)))

cat(sprintf('mean log2 LFQ intensity (na.rm over features): complete-feature subset %.2f vs dropped subset %.2f (delta %.2f)\n',
            mean(mean_abund_complete, na.rm = TRUE), mean(mean_abund_incomplete, na.rm = TRUE),
            mean(mean_abund_complete, na.rm = TRUE) - mean(mean_abund_incomplete, na.rm = TRUE)))
cat(sprintf('median detected-samples-per-feature (of 8): complete %.1f vs dropped %.1f\n',
            median(n_detected_complete), median(n_detected_incomplete)))

wt <- wilcox.test(mean_abund_complete, mean_abund_incomplete[!is.nan(mean_abund_incomplete)])
cat(sprintf('Wilcoxon rank-sum on per-feature mean abundance, complete vs dropped (excl. 0/8-detected): W=%.0f, p=%.3g\n', wt$statistic, wt$p.value))

# "Well-detected" is true by construction (complete = detected in all 8/8 samples). The nontrivial
# empirical claim is the ABUNDANCE bias. Report the quantile position of the complete-feature
# subset's abundance distribution within the full matrix.
full_mean <- rowMeans(M, na.rm = TRUE)
pct_complete_above_median <- mean(mean_abund_complete > median(full_mean, na.rm = TRUE))
cat(sprintf('%% of complete features above the whole-matrix median abundance: %.1f%%\n', 100 * pct_complete_above_median))
