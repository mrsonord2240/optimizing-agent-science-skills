source('F:/OpenScience/audits/bio-proteomics-differential-abundance/runs/common.R')
# INPUT 1 (Canonical): MaxQuant LFQ proteinGroups, 4 Control vs 4 Treatment, two acquisition days (batch).
# Code follows SKILL.md "limma Workflow (R)" and "DEqMS Workflow (R)" verbatim where possible.
suppressPackageStartupMessages({library(limma); library(DEqMS)})
cat('limma', as.character(packageVersion('limma')), '| DEqMS', as.character(packageVersion('DEqMS')), '\n')

sample_info <- read.csv(file.path(DATA, 'sample_annotation.csv'), stringsAsFactors = TRUE)
sample_info$condition <- factor(sample_info$condition, levels = c('Control', 'Treatment'))
pg <- read_pg()
protein_matrix <- lfq_log2(pg, as.character(sample_info$sample))
cat('Proteins after REV/CON/site removal:', nrow(protein_matrix), '\n')

# --- usage-guide step 1: assess missingness structure (how much, intensity-dependent?)
miss <- rowMeans(is.na(protein_matrix))
avg <- rowMeans(protein_matrix, na.rm = TRUE)
cat('Overall missing fraction:', round(mean(is.na(protein_matrix)), 3), '\n')
q <- cut(avg, quantile(avg, 0:4 / 4, na.rm = TRUE), include.lowest = TRUE)
print(round(tapply(miss, q, mean), 3))
allT <- rowSums(!is.na(protein_matrix[, sample_info$condition == 'Treatment'])) == 0
allC <- rowSums(!is.na(protein_matrix[, sample_info$condition == 'Control'])) == 0
cat('Absent in all Treatment runs:', sum(allT), '| absent in all Control runs:', sum(allC), '\n')

# --- SKILL.md limma block (verbatim apart from object names already matching)
design <- model.matrix(~0 + condition + batch, data = sample_info)  # batch in the model, not removed first
colnames(design)[1:2] <- levels(factor(sample_info$condition))
print(colnames(design))

run_skill_limma <- function(protein_matrix) {
  fit <- lmFit(protein_matrix, design)
  contrast_matrix <- makeContrasts(Treatment - Control, levels = design)
  fit2 <- contrasts.fit(fit, contrast_matrix)
  fit2 <- eBayes(fit2, trend = TRUE, robust = TRUE)  # trend mandatory for label-free; robust Winsorizes outliers
  fit2
}
fit2 <- tryCatch(run_skill_limma(protein_matrix), error = function(e) {
  cat('SKILL limma block as written FAILED (verbatim):', conditionMessage(e), '\n'); NULL })
if (is.null(fit2)) {
  # Adaptation (not in the Skill): MaxQuant writes rows whose LFQ is 0 in every run; they give Amean = NA,
  # which breaks eBayes(trend=TRUE). Minimal fix = drop rows with no observation at all.
  keep <- rowSums(!is.na(protein_matrix)) > 0
  cat('Adaptation: dropping', sum(!keep), 'all-missing rows and re-running the same block\n')
  protein_matrix <- protein_matrix[keep, ]
  fit2 <- run_skill_limma(protein_matrix)
}
cat('eBayes df.prior (median):', round(median(fit2$df.prior), 2), '\n')

results <- topTable(fit2, coef = 1, number = Inf, adjust.method = 'BH')
cat('topTable rows:', nrow(results), '| rows with NA logFC:', sum(is.na(results$logFC)), '\n')
sig <- rownames(results)[!is.na(results$adj.P.Val) & results$adj.P.Val < 0.05]
tested <- rownames(results)[!is.na(results$P.Value)]
score_calls(sig, tested, 'limma trend+robust, ~0+condition+batch')

# what happened to the 12 on/off proteins?
oo <- truth$protein[truth$class == 'on_off']
print(results[oo, c('logFC', 'AveExpr', 't', 'P.Value', 'adj.P.Val')])

# batch-ignored comparison (to show what the batch covariate buys)
d0 <- model.matrix(~0 + condition, data = sample_info); colnames(d0) <- levels(sample_info$condition)
f0 <- eBayes(suppressWarnings(contrasts.fit(lmFit(protein_matrix, d0), makeContrasts(Treatment - Control, levels = d0))), trend = TRUE, robust = TRUE)
r0 <- topTable(f0, number = Inf)
score_calls(rownames(r0)[!is.na(r0$adj.P.Val) & r0$adj.P.Val < 0.05], rownames(r0)[!is.na(r0$P.Value)], 'limma trend+robust, NO batch term')

# --- SKILL.md DEqMS block: label-free -> peptide count (Razor + unique peptides)
psm_count_per_protein <- setNames(pg$`Razor + unique peptides`, pg$acc)
fit2$count <- psm_count_per_protein[rownames(fit2$coefficients)]  # PSM for TMT, peptide for LFQ; min across batches
res_deqms <- tryCatch({
  fit3 <- spectraCounteBayes(fit2)
  outputResult(fit3, coef_col = 1)
}, error = function(e) { cat('DEqMS ERROR (verbatim):', conditionMessage(e), '\n'); NULL })
if (is.null(res_deqms)) {
  # adaptation: drop proteins whose contrast/sigma is not estimable (NA) before spectraCounteBayes
  ok <- !is.na(fit2$sigma) & !is.na(fit2$coefficients[, 1])
  cat('Adaptation: subsetting fit2 to', sum(ok), 'estimable proteins\n')
  f2 <- fit2[ok, ]
  f2 <- eBayes(f2, trend = TRUE, robust = TRUE)
  f2$count <- psm_count_per_protein[rownames(f2$coefficients)]
  fit3 <- spectraCounteBayes(f2)
  res_deqms <- outputResult(fit3, coef_col = 1)
}
cat('outputResult columns:', paste(colnames(res_deqms), collapse = ', '), '\n')
cat('outputResult rows:', nrow(res_deqms), '| NA sca.adj.pval:', sum(is.na(res_deqms$sca.adj.pval)),
    '| rownames are accessions:', all(rownames(res_deqms) %in% pg$acc), '\n')
sig_d <- rownames(res_deqms)[which(res_deqms$sca.adj.pval < 0.05)]
score_calls(sig_d, rownames(res_deqms)[!is.na(res_deqms$sca.P.Value)], 'DEqMS on NA-containing fit (as written)')
print(summary(fit3$sca.dfprior)); cat('length(sca.dfprior)', length(fit3$sca.dfprior), '\n')
# Check: is the per-row DEqMS moderation aligned? compare on the subset with complete estimable rows
okr <- !is.na(fit2$coefficients[, 1]) & !is.na(fit2$sigma)
f2c <- eBayes(fit2[okr, ], trend = TRUE, robust = TRUE)
f2c$count <- psm_count_per_protein[rownames(f2c$coefficients)]
res_c <- outputResult(spectraCounteBayes(f2c), coef_col = 1)
score_calls(rownames(res_c)[which(res_c$sca.adj.pval < 0.05)], rownames(res_c), 'DEqMS on estimable rows only')
score_calls(rownames(res_c)[which(res_c$adj.P.Val < 0.05)], rownames(res_c), 'limma (same rows) for reference')

# final table for the user (top 10)
out <- results[!is.na(results$P.Value), ]
out$gene <- pg$`Gene names`[match(rownames(out), pg$acc)]
write.csv(out, 'F:/OpenScience/audits/bio-proteomics-differential-abundance/runs/input1_limma_results.csv')
print(head(out[, c('gene', 'logFC', 'AveExpr', 't', 'P.Value', 'adj.P.Val')], 10))
