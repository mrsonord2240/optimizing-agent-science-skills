source('F:/OpenScience/audits/bio-proteomics-differential-abundance/runs/common.R')
# Lead 3: Skill-recommended methods vs downshift-imputation + limma, scored against the synthetic truth.
# Also tests the Skill's MECHANISM claim: "all imputed B values from one 0.3-sigma Gaussian -> collapsed
# within-group SD -> enormous t".
suppressPackageStartupMessages({library(limma); library(DEqMS); library(proDA)})
sample_info <- read.csv(file.path(DATA, 'sample_annotation.csv'), stringsAsFactors = TRUE)
sample_info$condition <- factor(sample_info$condition, levels = c('Control', 'Treatment'))
pg <- read_pg()
pm <- lfq_log2(pg, as.character(sample_info$sample))
pm <- pm[rowSums(!is.na(pm)) > 0, ]
C <- 1:4; T <- 5:8
nC <- rowSums(!is.na(pm[, C])); nT <- rowSums(!is.na(pm[, T]))
design <- model.matrix(~0 + condition + batch, data = sample_info); colnames(design)[1:2] <- c('Control', 'Treatment')
cm <- makeContrasts(Treatment - Control, levels = design)
lim <- function(m) topTable(eBayes(suppressWarnings(contrasts.fit(lmFit(m, design), cm)), trend = TRUE, robust = TRUE), number = Inf)

cat('--- Mechanism check (Perseus downshift parameters per sample) ---\n')
for (j in c(1, 5)) {
  x <- pm[, j]; cat(sprintf('%s: across-protein SD sigma = %.2f -> imputed SD 0.3*sigma = %.2f ; imputed mean = %.2f (sample median %.2f)\n',
                            colnames(pm)[j], sd(x, na.rm = TRUE), 0.3 * sd(x, na.rm = TRUE), mean(x, na.rm = TRUE) - 1.8 * sd(x, na.rm = TRUE), median(x, na.rm = TRUE)))
}
wsd <- apply(pm[nC == 4 & nT == 4, ], 1, function(v) mean(c(sd(v[C]), sd(v[T]))))
cat(sprintf('Real within-group replicate SD (complete proteins, median): %.2f\n\n', median(wsd)))

downshift <- function(m, shift = 1.8, width = 0.3) {
  for (j in seq_len(ncol(m))) { x <- m[, j]; mu <- mean(x, na.rm = TRUE); s <- sd(x, na.rm = TRUE)
    m[is.na(x), j] <- rnorm(sum(is.na(x)), mu - shift * s, width * s) }
  m
}
filters <- list('>=3 valid of 8' = rowSums(!is.na(pm)) >= 3,
                '>=3 valid in at least one group' = (nC >= 3 | nT >= 3),
                '>=2 valid in at least one group' = (nC >= 2 | nT >= 2))
res <- data.frame()
for (fn in names(filters)) for (seed in 1:5) {
  set.seed(seed); keep <- filters[[fn]]
  r <- lim(downshift(pm[keep, ]))
  called <- rownames(r)[r$adj.P.Val < 0.05]
  cl <- truth[called, 'class']; os <- called[(nC[called] == 0) | (nT[called] == 0)]
  res <- rbind(res, data.frame(filter = fn, seed = seed, tested = nrow(r), called = length(called), FP = sum(cl == 'null'),
                               FDR = round(100 * mean(cl == 'null'), 1), up = sum(cl == 'up'), down = sum(cl == 'down'),
                               onoff = sum(cl == 'on_off'), one_sided_called = length(os),
                               one_sided_null_FP = sum(truth[os, 'class'] == 'null')))
}
cat('--- Downshift(1.8/0.3) + limma trend+robust (~0+condition+batch), 5 imputation seeds per filter ---\n')
print(res, row.names = FALSE)
cat('\nSeed-to-seed spread in number called, per filter:\n'); print(aggregate(called ~ filter, res, range))

cat('\n--- Skill-recommended methods (same data, all-NA rows dropped) ---\n')
rl <- lim(pm)
score_calls(rownames(rl)[which(rl$adj.P.Val < 0.05)], rownames(rl)[!is.na(rl$P.Value)], 'limma trend+robust + batch (no imputation)')
fz <- suppressWarnings(contrasts.fit(lmFit(pm, design), cm))
ok <- rownames(pm)[!is.na(fz$coefficients[, 1]) & fz$df.residual > 0]   # DEqMS loess drops NA-sigma rows -> misaligned y.pred otherwise
f2 <- eBayes(suppressWarnings(contrasts.fit(lmFit(pm[ok, ], design), cm)), trend = TRUE, robust = TRUE)
f2$count <- setNames(pg$`Razor + unique peptides`, pg$acc)[rownames(f2$coefficients)]
rd <- outputResult(spectraCounteBayes(f2), coef_col = 1)
score_calls(rownames(rd)[which(rd$sca.adj.pval < 0.05)], rownames(rd), 'DEqMS (Razor+unique peptides), estimable rows')
set.seed(42)
fp <- proDA(pm, design = ~condition + batch, col_data = sample_info, reference_level = 'Control')
rp <- test_diff(fp, 'conditionTreatment')
score_calls(rp$name[which(rp$adj_pval < 0.05)], rp$name, 'proDA ~condition+batch')
cat('\nproDA diff for proteins absent in all T, by class (median diff / median se):\n')
a <- rp[rp$name %in% rownames(pm)[nT == 0], ]; a$class <- truth[a$name, 'class']
print(aggregate(cbind(diff, se) ~ class, a, median))
cat('Downshift logFC for the same proteins (seed 1, filter >=3 in one group), by class:\n')
set.seed(1); keep <- filters[[2]]; r1 <- lim(downshift(pm[keep, ]))
b <- r1[rownames(r1) %in% rownames(pm)[nT == 0], ]; b$class <- truth[rownames(b), 'class']
print(aggregate(cbind(logFC, P.Value) ~ class, b, median))
cat('True log2FC of the absent-in-T down proteins (median):', round(median(truth[rownames(b)[b$class == 'down'], 'true_log2fc']), 2), '\n')
