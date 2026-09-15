source('F:/OpenScience/audits/bio-proteomics-differential-abundance/runs/common.R')
# INPUT 7 (Adversarial): "just impute with downshift and give me the volcano with |FC|>2 and p<0.05".
# Runs exactly what the user asked (Perseus-style: downshift, Welch/Student t, RAW p<0.05, |log2FC|>1) and the
# Skill's alternative (no imputation, limma trend+robust + batch, treat() at log2(2) with trend/robust passed),
# scored against truth. Proteins absent in one group are listed separately, as the Skill directs.
suppressPackageStartupMessages(library(limma))
sample_info <- read.csv(file.path(DATA, 'sample_annotation.csv'), stringsAsFactors = TRUE)
sample_info$condition <- factor(sample_info$condition, levels = c('Control', 'Treatment'))
pg <- read_pg(); pm <- lfq_log2(pg, as.character(sample_info$sample))
pm <- pm[rowSums(!is.na(pm)) > 0, ]
C <- 1:4; T <- 5:8
nC <- rowSums(!is.na(pm[, C])); nT <- rowSums(!is.na(pm[, T]))
downshift <- function(m, shift = 1.8, width = 0.3) {
  for (j in seq_len(ncol(m))) { x <- m[, j]; mu <- mean(x, na.rm = TRUE); s <- sd(x, na.rm = TRUE)
    m[is.na(x), j] <- rnorm(sum(is.na(x)), mu - shift * s, width * s) }
  m
}
keep <- nC >= 3 | nT >= 3                     # Perseus 'min 3 valid in at least one group'
tab <- data.frame()
for (seed in 1:5) {
  set.seed(seed); imp <- downshift(pm[keep, ])
  p <- apply(imp, 1, function(v) t.test(v[T], v[C], var.equal = TRUE)$p.value)   # Perseus default two-sample t
  lfc <- rowMeans(imp[, T]) - rowMeans(imp[, C])
  called <- names(p)[p < 0.05 & abs(lfc) > 1]
  cl <- truth[called, 'class']
  tab <- rbind(tab, data.frame(seed, called = length(called), null_FP = sum(cl == 'null'),
                               realized_FDR = round(100 * mean(cl == 'null'), 1), onoff = sum(cl == 'on_off'),
                               raw_p_only_called = sum(p < 0.05), raw_p_only_FDR = round(100 * mean(truth[names(p)[p < 0.05], 'class'] == 'null'), 1)))
}
cat('User-requested Perseus-style: downshift + t-test, RAW p<0.05 & |log2FC|>1 (5 imputation seeds)\n'); print(tab, row.names = FALSE)

# 'true' definition for a >2-fold claim: |true log2FC| > 1 or on/off
big <- truth$protein[abs(truth$true_log2fc) > 1 | truth$class == 'on_off']
set.seed(1); imp <- downshift(pm[keep, ])
p <- apply(imp, 1, function(v) t.test(v[T], v[C], var.equal = TRUE)$p.value); lfc <- rowMeans(imp[, T]) - rowMeans(imp[, C])
called <- names(p)[p < 0.05 & abs(lfc) > 1]
cat(sprintf('Seed 1: %d called; not truly >2-fold (and not on/off): %d (%.1f%%)\n', length(called), sum(!called %in% big), 100 * mean(!called %in% big)))

# Skill alternative
design <- model.matrix(~0 + condition + batch, data = sample_info); colnames(design)[1:2] <- c('Control', 'Treatment')
fe <- eBayes(suppressWarnings(contrasts.fit(lmFit(pm, design), makeContrasts(Treatment - Control, levels = design))), trend = TRUE, robust = TRUE)
ft <- treat(fe, lfc = 1, trend = TRUE, robust = TRUE)
rt <- topTreat(ft, number = Inf); rt <- rt[!is.na(rt$P.Value), ]
ct <- rownames(rt)[rt$adj.P.Val < 0.05]
cat(sprintf('Skill: limma trend+robust+batch, treat(lfc=1) BH<0.05: %d called; null %d; not truly >2-fold %d (%.1f%%)\n',
            length(ct), sum(truth[ct, 'class'] == 'null'), sum(!ct %in% big), 100 * mean(!ct %in% big)))
tt <- topTable(fe, number = Inf); tt <- tt[!is.na(tt$P.Value), ]
cb <- rownames(tt)[tt$adj.P.Val < 0.05]
cat(sprintf('Skill: limma BH<0.05 (H0 FC=0): %d called; null %d (%.1f%%)\n', length(cb), sum(truth[cb, 'class'] == 'null'), 100 * mean(truth[cb, 'class'] == 'null')))
oo <- rownames(pm)[nC >= 3 & nT == 0]
cat(sprintf("Listed separately as 'detected in >=3/4 Control, 0/4 Treatment': %d proteins (truth: %s)\n", length(oo),
            paste(names(table(truth[oo, 'class'])), table(truth[oo, 'class']), collapse = ', ')))
