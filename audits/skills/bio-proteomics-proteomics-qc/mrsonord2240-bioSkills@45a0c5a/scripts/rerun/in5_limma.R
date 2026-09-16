.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# Re-audit 2026-09-15, Input 5 sensitivity: batch in design (Skill's preferred route) with and without T4.
# limma used only to measure how the QC decisions move the hit list; truth from SYNTHETIC truth_proteins.csv.
suppressPackageStartupMessages(library(limma))
R <- 'F:/OpenScience/audits/bio-proteomics-proteomics-qc'
m <- as.matrix(read.csv(file.path(R, 'rerun/out_in5/log2_lfq_failed_filtered.csv'), row.names = 1, check.names = FALSE))
info <- read.csv(file.path(R, 'data/sample_annotation.csv'), row.names = 1)
truth <- read.csv(file.path(R, 'data/truth_proteins.csv')); da <- truth$protein[truth$class %in% c('up', 'down')]
run <- function(samples, with_batch) {
  d <- info[samples, ]; cond <- factor(d$condition, levels = c('Control', 'Treatment')); b <- factor(d$batch)
  des <- if (with_batch) model.matrix(~ cond + b) else model.matrix(~ cond)
  tt <- topTable(eBayes(lmFit(m[, samples], des)), coef = 'condTreatment', number = Inf, sort.by = 'none')
  sig <- rownames(tt)[!is.na(tt$adj.P.Val) & tt$adj.P.Val < 0.05]
  list(row = data.frame(samples = ifelse(length(samples) == 8, 'all 8', 'drop T4'), batch = with_batch, n_sig = length(sig),
                        true_pos = sum(sig %in% da), false_pos = sum(!sig %in% da)), sig = sig)
}
a8 <- colnames(m); n4 <- setdiff(a8, 'T4')
r <- list(run(a8, FALSE), run(a8, TRUE), run(n4, FALSE), run(n4, TRUE))
print(do.call(rbind, lapply(r, `[[`, 'row')), row.names = FALSE)
x <- r[[2]]$sig; y <- r[[4]]$sig
cat(sprintf('batch in design: all8 %d, dropT4 %d, shared %d, Jaccard %.2f\n', length(x), length(y), length(intersect(x, y)), length(intersect(x, y)) / length(union(x, y))))
