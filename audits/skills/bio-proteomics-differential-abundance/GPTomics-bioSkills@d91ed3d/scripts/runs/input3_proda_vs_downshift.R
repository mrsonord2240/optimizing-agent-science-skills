source('F:/OpenScience/audits/bio-proteomics-differential-abundance/runs/common.R')
# INPUT 3 (Edge): heavy MNAR missingness / on-off proteins. SKILL.md "proDA Workflow (R)" verbatim first,
# then the comparison the Skill argues against: Perseus-style downshift imputation + limma.
suppressPackageStartupMessages({library(limma); library(proDA)})
cat('proDA', as.character(packageVersion('proDA')), '| limma', as.character(packageVersion('limma')), '\n')
set.seed(42)
sample_info <- read.csv(file.path(DATA, 'sample_annotation.csv'), stringsAsFactors = TRUE)
sample_info$condition <- factor(sample_info$condition, levels = c('Control', 'Treatment'))
pg <- read_pg()
protein_matrix <- lfq_log2(pg, as.character(sample_info$sample))
cls <- truth[rownames(protein_matrix), 'class']
nT <- rowSums(!is.na(protein_matrix[, 5:8])); nC <- rowSums(!is.na(protein_matrix[, 1:4]))
cat('Absent in all T:', sum(nT == 0 & nC > 0), '(truth: ', paste(names(table(cls[nT == 0 & nC > 0])), table(cls[nT == 0 & nC > 0]), collapse = ', '), ')\n')
cat('Absent in all C:', sum(nC == 0 & nT > 0), '(truth: ', paste(names(table(cls[nC == 0 & nT > 0])), table(cls[nC == 0 & nT > 0]), collapse = ', '), ')\n')
cat('No value at all:', sum(nC == 0 & nT == 0), '\n')

# ---------------- SKILL.md proDA block, verbatim
t0 <- Sys.time()
fit <- proDA(protein_matrix, design = ~condition, col_data = sample_info,
             reference_level = 'Control')
cat('proDA fit time:', round(as.numeric(difftime(Sys.time(), t0, units = 'secs')), 1), 's\n')
cat('result_names(fit):', paste(result_names(fit), collapse = ', '), '\n')
results <- tryCatch(test_diff(fit, conditionTreatment - conditionControl),
                    error = function(e) { cat('SKILL test_diff call FAILED (verbatim):', conditionMessage(e), '\n'); NULL })
if (is.null(results)) {
  # Adaptation: with reference_level='Control' the treatment effect IS the coefficient conditionTreatment
  results <- test_diff(fit, 'conditionTreatment')
  cat('Adaptation: test_diff(fit, "conditionTreatment")\n')
}
cat('test_diff columns:', paste(colnames(results), collapse = ', '), '\n')
rownames(results) <- results$name
ok <- !is.na(results$pval)
score_calls(results$name[which(results$adj_pval < 0.05)], results$name[ok], 'proDA ~condition (Skill block, adapted contrast)')

# proDA with batch in the design (Skill decision tree: batch as covariate)
fitb <- proDA(protein_matrix, design = ~condition + batch, col_data = sample_info, reference_level = 'Control')
cat('result_names(fitb):', paste(result_names(fitb), collapse = ', '), '\n')
rb <- test_diff(fitb, 'conditionTreatment'); rownames(rb) <- rb$name
score_calls(rb$name[which(rb$adj_pval < 0.05)], rb$name[!is.na(rb$pval)], 'proDA ~condition+batch')

# How proDA treats groups of proteins absent in all Treatment runs
grpT0 <- rownames(protein_matrix)[nT == 0 & nC > 0]
tab <- data.frame(class = truth[grpT0, 'class'], nC = nC[grpT0], diff = round(rb[grpT0, 'diff'], 2),
                  se = round(rb[grpT0, 'se'], 2), adj_p = signif(rb[grpT0, 'adj_pval'], 2))
cat('\nproDA (~condition+batch) on proteins absent in all T, by truth class:\n')
print(aggregate(cbind(called = adj_p < 0.05) ~ class, data = tab, FUN = function(x) paste0(sum(x), '/', length(x))))
print(head(tab[order(tab$class), ], 16))

# ---------------- The approach the Skill warns against: Perseus downshift (width 0.3, shift 1.8) + limma
downshift <- function(m, shift = 1.8, width = 0.3) {
  for (j in seq_len(ncol(m))) {
    x <- m[, j]; mu <- mean(x, na.rm = TRUE); s <- sd(x, na.rm = TRUE)
    m[is.na(x), j] <- rnorm(sum(is.na(x)), mu - shift * s, width * s)
  }
  m
}
set.seed(42)
keep <- rowSums(!is.na(protein_matrix)) >= 3        # a typical Perseus valid-value filter (3 of 8)
imp <- downshift(protein_matrix[keep, ])
design <- model.matrix(~0 + condition + batch, data = sample_info)
colnames(design)[1:2] <- levels(factor(sample_info$condition))
fi <- eBayes(contrasts.fit(lmFit(imp, design), makeContrasts(Treatment - Control, levels = design)), trend = TRUE, robust = TRUE)
ri <- topTable(fi, number = Inf)
score_calls(rownames(ri)[ri$adj.P.Val < 0.05], rownames(ri), 'downshift(1.8/0.3) + limma trend+robust')
# same rows, proDA, for a like-for-like comparison
same <- rownames(ri)
score_calls(same[which(rb[same, 'adj_pval'] < 0.05)], same, 'proDA ~condition+batch on the same rows')

# Anchor/wing check: proteins absent in all of one group after downshift
one_side <- rownames(imp)[(nT[rownames(imp)] == 0) | (nC[rownames(imp)] == 0)]
w <- ri[one_side, ]
cat('\nDownshift: proteins absent in all of one group:', length(one_side), '| called at adj.P<0.05:', sum(w$adj.P.Val < 0.05),
    '| of which null:', sum(w$adj.P.Val < 0.05 & truth[one_side, 'class'] == 'null'), '\n')
cat('  |logFC| of these (quantiles):', round(quantile(abs(w$logFC), c(.1, .5, .9)), 2),
    '| SD of within-group imputed values (median):', round(median(apply(imp[one_side, 5:8], 1, sd)[nT[one_side] == 0]), 3), '\n')
cat('  -log10 P quantiles:', round(quantile(-log10(w$P.Value), c(.1, .5, .9)), 1), '\n')
cat('  Correlation of logFC with AveExpr among them (streak => strong):', round(cor(w$logFC[w$logFC < 0], w$AveExpr[w$logFC < 0]), 2), '\n')
# save volcano data for inspection
vol <- data.frame(protein = rownames(ri), logFC = ri$logFC, mlog10p = -log10(ri$P.Value),
                  one_side = rownames(ri) %in% one_side, class = truth[rownames(ri), 'class'])
write.csv(vol, 'F:/OpenScience/audits/bio-proteomics-differential-abundance/runs/input3_downshift_volcano.csv', row.names = FALSE)
pv <- data.frame(protein = rb$name, diff = rb$diff, mlog10p = -log10(rb$pval),
                 one_side = rb$name %in% one_side | rb$name %in% grpT0, class = truth[rb$name, 'class'])
write.csv(pv, 'F:/OpenScience/audits/bio-proteomics-differential-abundance/runs/input3_proda_volcano.csv', row.names = FALSE)
