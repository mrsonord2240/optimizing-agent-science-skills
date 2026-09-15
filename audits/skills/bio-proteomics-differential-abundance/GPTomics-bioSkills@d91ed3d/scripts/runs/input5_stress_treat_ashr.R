.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# INPUT 5 (Stress): 3 arms x 3 unbalanced days, two contrasts, >=1.5-fold at 5% FDR via treat(), ashr for the figure,
# raw FC for GSEA. SKILL.md limma / treat / ashr blocks followed as written; adaptations are marked.
suppressPackageStartupMessages({library(limma); library(ashr)})
cat('limma', as.character(packageVersion('limma')), '| ashr', as.character(packageVersion('ashr')), '\n')
D <- 'F:/OpenScience/audits/bio-proteomics-differential-abundance/data'
protein_matrix <- as.matrix(read.csv(file.path(D, 'three_arm_log2.csv'), row.names = 1))
sample_info <- read.csv(file.path(D, 'three_arm_samples.csv'), stringsAsFactors = TRUE)
sample_info$condition <- factor(sample_info$condition, levels = c('Control', 'DrugA', 'DrugB'))
tru <- read.csv(file.path(D, 'three_arm_truth.csv'), row.names = 1)
stopifnot(identical(colnames(protein_matrix), as.character(sample_info$sample)))
print(table(sample_info$condition, sample_info$batch))

design <- model.matrix(~0 + condition + batch, data = sample_info)
colnames(design)[1:2] <- levels(factor(sample_info$condition))     # SKILL line, verbatim (hard-codes 2 groups)
cat('design columns after the Skill rename:', paste(colnames(design), collapse = ', '), '\n')
mk <- tryCatch(makeContrasts(DrugA - Control, DrugB - Control, levels = design),
               error = function(e) { cat('makeContrasts with Skill naming FAILED (verbatim):', conditionMessage(e), '\n'); NULL })
colnames(design)[1:3] <- levels(sample_info$condition)             # adaptation: 3 groups
contrast_matrix <- makeContrasts(DrugA - Control, DrugB - Control, levels = design)

fit <- lmFit(protein_matrix, design)
fit2 <- contrasts.fit(fit, contrast_matrix)
fit2 <- tryCatch(eBayes(fit2, trend = TRUE, robust = TRUE),
                 error = function(e) { cat('eBayes(trend=TRUE, robust=TRUE) FAILED (verbatim):', conditionMessage(e), '\n'); NULL })
if (is.null(fit2)) {
  # adaptation: valid-value filter (>=3 of 4 in at least one arm) - the Skill gives no filtering step
  nv <- sapply(levels(sample_info$condition), function(g) rowSums(!is.na(protein_matrix[, sample_info$condition == g])))
  keep <- apply(nv >= 3, 1, any)
  cat('Adaptation: keeping', sum(keep), 'of', nrow(protein_matrix), 'proteins (>=3/4 valid in at least one arm)\n')
  protein_matrix <- protein_matrix[keep, ]
  fit <- lmFit(protein_matrix, design)
  fit2 <- eBayes(contrasts.fit(fit, contrast_matrix), trend = TRUE, robust = TRUE)
}
cat('df.prior range:', round(range(fit2$df.prior), 2), '| s2.prior varies with intensity:', length(unique(round(fit2$s2.prior, 4))) > 1, '\n')
fit_eb <- fit2   # keep the eBayes fit (the Skill overwrites fit2 with treat())

tau <- log2(1.5)
eval_set <- function(called, coef, label) {
  tfc <- tru[called, ifelse(coef == 1, 'fc_DrugA', 'fc_DrugB')]
  fdr_nz <- mean(tfc == 0); fdr_tau <- mean(abs(tfc) <= tau)
  cat(sprintf('%-52s called=%3d  null(0)=%3d  |trueFC|<=1.5x=%3d  FDR vs H0:|FC|<=1.5x = %5.1f%%\n', label, length(called),
              sum(tfc == 0), sum(abs(tfc) <= tau), 100 * ifelse(length(called), fdr_tau, 0)))
}
for (k in 1:2) {
  cn <- colnames(contrast_matrix)[k]; cat('\n====', cn, '====  true |FC|>1.5x among tested:',
    sum(abs(tru[rownames(protein_matrix), k]) > tau, na.rm = TRUE), '\n')
  tt <- topTable(fit_eb, coef = k, number = Inf, adjust.method = 'BH')
  tt <- tt[!is.na(tt$P.Value), ]
  eval_set(rownames(tt)[tt$adj.P.Val < 0.05], k, 'topTable adj.P<0.05 (H0: FC=0)')
  eval_set(rownames(tt)[tt$adj.P.Val < 0.05 & abs(tt$logFC) > tau], k, 'double filter adj.P<0.05 & |logFC|>log2(1.5)')
  tl <- topTable(fit_eb, coef = k, number = Inf, lfc = tau); eval_set(rownames(tl)[tl$adj.P.Val < 0.05], k, 'topTable(lfc=log2(1.5))')
  # SKILL treat block, verbatim
  LFC_THRESHOLD <- log2(1.5)
  fit2 <- treat(fit_eb, lfc = LFC_THRESHOLD)
  results <- topTreat(fit2, coef = k, number = Inf)  # topTreat omits the B column
  if (k == 1) cat('topTreat columns:', paste(colnames(results), collapse = ', '), '\n')
  results <- results[!is.na(results$P.Value), ]
  eval_set(rownames(results)[results$adj.P.Val < 0.05], k, 'treat(lfc=log2(1.5)) + topTreat adj.P<0.05 (Skill)')
  ft <- treat(fit_eb, lfc = LFC_THRESHOLD, trend = TRUE, robust = TRUE)
  rt <- topTreat(ft, coef = k, number = Inf); rt <- rt[!is.na(rt$P.Value), ]
  eval_set(rownames(rt)[rt$adj.P.Val < 0.05], k, 'treat(lfc, trend=TRUE, robust=TRUE) + topTreat')
}
cat('\nargs(treat):\n'); print(args(treat))
cat('s2.prior: eBayes(trend) range', round(range(fit_eb$s2.prior), 4), '| Skill treat() fit', round(range(fit2$s2.prior), 4), '\n')
cat('df.prior: eBayes(trend,robust) range', round(range(fit_eb$df.prior), 1), '| Skill treat() fit', round(range(fit2$df.prior), 1), '\n')

# SKILL ashr block, verbatim (uses fit2 - which the Skill's own treat block has just overwritten)
cat('\n---- ashr ----\n')
sh <- tryCatch({
  se <- sqrt(fit2$s2.post) * fit2$stdev.unscaled[, 1]
  shrunk <- ash(fit2$coefficients[, 1], se, mixcompdist = 'normal')
  shrunk
}, error = function(e) { cat('ashr block FAILED (verbatim):', conditionMessage(e), '\n'); NULL })
if (is.null(sh)) {
  ok <- !is.na(fit2$coefficients[, 1]) & !is.na(fit2$s2.post)
  cat('Adaptation: dropping', sum(!ok), 'rows with NA coefficient / s2.post before ash()\n')
  se <- sqrt(fit2$s2.post[ok]) * fit2$stdev.unscaled[ok, 1]
  sh <- ash(fit2$coefficients[ok, 1], se, mixcompdist = 'normal')
  names_ok <- rownames(fit2$coefficients)[ok]
} else names_ok <- rownames(fit2$coefficients)
cat('treat() fit has s2.post:', !is.null(fit2$s2.post), '| identical to eBayes s2.post:', isTRUE(all.equal(fit2$s2.post, fit_eb$s2.post)), '\n')
shrunken_fc <- sh$result$PosteriorMean
lfsr <- sh$result$lfsr
cat('ash() rows returned:', nrow(sh$result), '| NA PosteriorMean:', sum(is.na(shrunken_fc)), '\n')
cc <- !is.na(fit2$coefficients[names_ok, 1]) & !is.na(shrunken_fc)
names_ok <- names_ok[cc]; shrunken_fc <- shrunken_fc[cc]; lfsr <- lfsr[cc]
raw <- fit2$coefficients[names_ok, 1]; truthA <- tru[names_ok, 'fc_DrugA']
cat(sprintf('DrugA: RMSE vs truth  raw logFC = %.3f | ashr PosteriorMean = %.3f\n', sqrt(mean((raw - truthA)^2)), sqrt(mean((shrunken_fc - truthA)^2))))
cat(sprintf('DrugA: null proteins |raw| mean %.3f -> |shrunk| mean %.3f ; lfsr<0.05: %d (null among them %d)\n',
            mean(abs(raw[truthA == 0])), mean(abs(shrunken_fc[truthA == 0])), sum(lfsr < 0.05), sum(lfsr < 0.05 & truthA == 0)))
cat('pi0 (null mass) estimated by ash:', round(get_pi0(sh), 3), '| true null fraction among tested:', round(mean(truthA == 0), 3), '\n')

# GSEA ranking: raw logFC (Skill: report raw FC for ranking; do not threshold)
gsea_rank <- sort(setNames(fit_eb$t[, 1], rownames(fit_eb$t))[!is.na(fit_eb$t[, 1])], decreasing = TRUE)
cat('GSEA rank vector (moderated t, DrugA):', length(gsea_rank), 'proteins, all tested proteins retained\n')
