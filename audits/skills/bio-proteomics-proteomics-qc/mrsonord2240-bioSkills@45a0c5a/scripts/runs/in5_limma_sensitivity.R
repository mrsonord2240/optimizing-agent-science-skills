.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# Input 5 sensitivity check (usage-guide Tips: "run a sensitivity check with and without borderline samples";
# SKILL.md PCA section: "include batch in the design matrix downstream"). The test itself routes to
# differential-abundance; limma is used here only to measure how the QC decisions move the hit list.
# Truth from SYNTHETIC truth_proteins.csv is used to score the configurations. Audit 2026-09-11.
suppressPackageStartupMessages(library(limma))
R <- 'F:/OpenScience/audits/bio-proteomics-proteomics-qc'
m <- as.matrix(read.csv(file.path(R, 'runs/out_in5/log2_lfq_failed_filtered.csv'), row.names = 1, check.names = FALSE))
info <- read.csv(file.path(R, 'data/sample_annotation.csv'), row.names = 1)
truth <- read.csv(file.path(R, 'data/truth_proteins.csv'))
da <- truth$protein[truth$class %in% c('up', 'down')]
run <- function(samples, with_batch) {
  x <- m[, samples]; d <- info[samples, ]
  cond <- factor(d$condition, levels = c('Control', 'Treatment')); b <- factor(d$batch)
  des <- if (with_batch) model.matrix(~ cond + b) else model.matrix(~ cond)
  fit <- eBayes(lmFit(x, des))
  tt <- topTable(fit, coef = 'condTreatment', number = Inf, sort.by = 'none')
  sig <- rownames(tt)[!is.na(tt$adj.P.Val) & tt$adj.P.Val < 0.05]
  data.frame(samples = if (length(samples) == 8) 'all 8' else 'drop T4', batch_in_design = with_batch,
             n_sig = length(sig), true_pos = sum(sig %in% da), false_pos = sum(!sig %in% da),
             tested_DA = sum(rownames(tt) %in% da & !is.na(tt$P.Value)),
             sens = round(sum(sig %in% da) / sum(rownames(tt) %in% da & !is.na(tt$P.Value)), 3),
             df_prior = round(fit$df.prior, 2), sig = I(list(sig)))
}
all8 <- colnames(m); no4 <- setdiff(all8, 'T4')
res <- rbind(run(all8, FALSE), run(all8, TRUE), run(no4, FALSE), run(no4, TRUE))
print(res[, setdiff(names(res), 'sig')], row.names = FALSE)
a <- res$sig[[2]]; b <- res$sig[[4]]
cat(sprintf('\nOverlap of hit lists (batch in design): all8=%d, dropT4=%d, shared=%d, Jaccard=%.2f\n',
            length(a), length(b), length(intersect(a, b)), length(intersect(a, b)) / length(union(a, b))))
