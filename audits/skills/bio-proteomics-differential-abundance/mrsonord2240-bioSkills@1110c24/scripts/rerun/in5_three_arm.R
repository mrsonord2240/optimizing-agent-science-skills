# Input 5 (regression, stress): 3 arms x unbalanced days, two contrasts, >=1.5-fold via treat, ashr, GSEA list. SYNTHETIC.
source('F:/OpenScience/audits/bio-proteomics-differential-abundance/rerun/common.R')
suppressPackageStartupMessages(library(ashr))
X <- as.matrix(read.csv(file.path(RR, 'data', 'three_arm_log2.csv'), row.names = 1))
sample_info <- read.csv(file.path(RR, 'data', 'three_arm_samples.csv'))
tr <- read.csv(file.path(RR, 'data', 'three_arm_truth.csv'), row.names = 1)
protein_matrix <- X[, sample_info$sample]
cat('proteins:', nrow(protein_matrix), '| arms:', paste(unique(sample_info$condition), collapse = ','), '| day x arm:\n'); print(table(sample_info$condition, sample_info$batch))

# Skill limma block verbatim EXCEPT its contrast line names Treatment - Control; run the block's lines up to eBayes with
# the two-arm contrast replaced (the agent must choose the contrasts for three arms).
src <- readLines(list.files(BLK, pattern = '^b01', full.names = TRUE))
src <- sub('makeContrasts(Treatment - Control, levels = design)', 'makeContrasts(DrugA - Control, DrugB - Control, levels = design)', src, fixed = TRUE)
src <- sub('coef = 1,', 'coef = 1,', src, fixed = TRUE)
tf <- tempfile(fileext = '.R'); writeLines(src, tf)
res <- tryCatch({ sys.source(tf, envir = globalenv()); 'OK' }, error = function(e) paste('ERROR:', conditionMessage(e)))
cat('[limma block, contrast line adapted]', res, '\n')
cat('design columns:', paste(colnames(design), collapse = ','), '| rows kept by >=2-in-every-group filter:', nrow(protein_matrix), '\n')

LFC_THRESHOLD <- log2(1.5)
fit_treat <- treat(fit2, lfc = LFC_THRESHOLD, trend = TRUE, robust = TRUE)   # Skill treat line with lfc set to 1.5-fold
cat('treat s2.prior varies:', length(unique(round(fit_treat$s2.prior, 6))) > 1, '\n')
for (k in 1:2) {
  arm <- c('DrugA', 'DrugB')[k]
  tt <- topTreat(fit_treat, coef = k, number = Inf)
  hits <- rownames(tt)[tt$adj.P.Val < 0.05]
  fc <- tr[hits, paste0('fc_', arm)]
  cat(sprintf('%s treat 1.5-fold BH<0.05: %d called | truly |FC|<=log2(1.5): %d | truly zero: %d\n', arm, length(hits),
              sum(abs(fc) <= log2(1.5)), sum(fc == 0)))
  dbl <- topTable(fit2, coef = k, number = Inf); dh <- rownames(dbl)[dbl$adj.P.Val < 0.05 & abs(dbl$logFC) > log2(1.5)]
  cat(sprintf('   double filter (not Skill): %d called | truly |FC|<=log2(1.5): %d\n', length(dh), sum(abs(tr[dh, paste0('fc_', arm)]) <= log2(1.5))))
}
# ashr block verbatim, for coefficient 1 (DrugA - Control)
run_block('b06')
est <- fit2$coefficients[ok, 1]; true <- tr[names(est), 'fc_DrugA']
cat('ashr DrugA: RMSE raw', round(sqrt(mean((est - true)^2)), 3), '-> shrunk', round(sqrt(mean((shrunken_fc - true)^2)), 3),
    '| lfsr<0.05:', sum(lfsr < 0.05), '(null among them:', sum(lfsr < 0.05 & true == 0), ')\n')
rank_vec <- sort(setNames(fit2$t[, 1], rownames(fit2)), decreasing = TRUE)
cat('GSEA rank vector (moderated t, DrugA):', length(rank_vec), 'proteins, NA:', sum(is.na(rank_vec)), '\n')
