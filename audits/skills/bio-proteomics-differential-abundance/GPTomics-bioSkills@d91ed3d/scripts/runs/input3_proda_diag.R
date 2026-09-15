source('F:/OpenScience/audits/bio-proteomics-differential-abundance/runs/common.R')
# Why is proDA so much less powerful than limma here, and why are on/off diffs ~0?
suppressPackageStartupMessages({library(limma); library(proDA)})
set.seed(42)
sample_info <- read.csv(file.path(DATA, 'sample_annotation.csv'), stringsAsFactors = TRUE)
sample_info$condition <- factor(sample_info$condition, levels = c('Control', 'Treatment'))
pg <- read_pg()
pm <- lfq_log2(pg, as.character(sample_info$sample))
pm <- pm[rowSums(!is.na(pm)) > 0, ]                      # drop the 55 all-missing rows
fit <- proDA(pm, design = ~condition + batch, col_data = sample_info, reference_level = 'Control')
print(fit)
cat('\nhyper_parameters:\n'); str(hyper_parameters(fit))
cat('convergence:\n'); str(convergence(fit))
r <- test_diff(fit, 'conditionTreatment'); rownames(r) <- r$name
score_calls(r$name[which(r$adj_pval < 0.05)], r$name[!is.na(r$pval)], 'proDA ~condition+batch, all-NA rows dropped')
# compare SE and df on complete proteins with limma
comp <- rownames(pm)[rowSums(is.na(pm)) == 0]
design <- model.matrix(~0 + condition + batch, data = sample_info); colnames(design)[1:2] <- c('Control', 'Treatment')
fl <- eBayes(contrasts.fit(lmFit(pm[comp, ], design), makeContrasts(Treatment - Control, levels = design)), trend = TRUE, robust = TRUE)
se_l <- sqrt(fl$s2.post) * fl$stdev.unscaled[, 1]
cat('\nComplete proteins:', length(comp), '\n')
cat('median SE limma:', round(median(se_l), 3), '| median SE proDA:', round(median(r[comp, 'se']), 3), '\n')
cat('median df proDA:', round(median(r[comp, 'df']), 2), '| limma df.total:', round(median(fl$df.total), 1), '\n')
cat('cor(diff proDA, logFC limma):', round(cor(r[comp, 'diff'], fl$coefficients[, 1]), 4), '\n')
# per-protein sigma estimates
fp <- feature_parameters(fit)
cat('proDA feature_parameters columns:', paste(colnames(fp), collapse = ', '), '\n')
print(summary(fp$s2)); print(summary(fp$df))
cat('limma sigma^2 median (complete):', round(median(fl$sigma^2), 4), '| s2.prior:', round(fl$s2.prior[1], 4), '\n')
oo <- truth$protein[truth$class == 'on_off']; oo <- oo[oo %in% rownames(pm)]
cat('\nOn/off proteins under proDA:\n')
print(cbind(r[oo, c('diff', 'se', 'df', 'pval', 'adj_pval', 'n_obs')], ctrl_mean = round(rowMeans(pm[oo, 1:4], na.rm = TRUE), 2)))
cat('\nDropout curve per sample (rho, zeta):\n'); print(hyper_parameters(fit)[c('dropout_curve_position', 'dropout_curve_scale')])
