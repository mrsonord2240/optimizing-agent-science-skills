# Input 8 diagnostic: are the paired-design false positives proteins without complete donor pairs? SYNTHETIC data.
source('F:/OpenScience/audits/bio-proteomics-differential-abundance/rerun/common.R')
X <- as.matrix(read.csv(file.path(RR, 'data', 'paired_donor_log2.csv'), row.names = 1))
si <- read.csv(file.path(RR, 'data', 'paired_donor_samples.csv'))
truth <- read.csv(file.path(RR, 'data', 'paired_donor_truth.csv'))
si$condition <- factor(si$condition, levels = c('Unstim', 'LPS')); si$batch <- factor(si$donor)
X <- X[, si$sample]
pairs <- sapply(levels(si$batch), function(d) !is.na(X[, si$batch == d & si$condition == 'Unstim']) & !is.na(X[, si$batch == d & si$condition == 'LPS']))
n_pairs <- rowSums(pairs)
cond <- si$condition
nv <- sapply(levels(cond), function(g) rowSums(!is.na(X[, cond == g, drop = FALSE])))
keep_skill <- apply(nv >= 2, 1, all)
design <- model.matrix(~0 + condition + batch, data = si); colnames(design)[1:2] <- levels(cond)
fitA <- eBayes(contrasts.fit(lmFit(X[keep_skill, ], design), makeContrasts(LPS - Unstim, levels = design)), trend = TRUE, robust = TRUE)
tA <- topTable(fitA, number = Inf)
sig <- rownames(tA)[tA$adj.P.Val < 0.05]
cls <- truth$class[match(sig, truth$protein)]
cat('Skill filter: called', length(sig), '| complete pairs among null FPs:', paste(n_pairs[sig[cls == 'null']], collapse = ','), '\n')
cat('complete pairs among true hits (median):', median(n_pairs[sig[cls != 'null']]), '\n')
keep_pairs <- n_pairs >= 2
fitB <- eBayes(contrasts.fit(lmFit(X[keep_pairs, ], design), makeContrasts(LPS - Unstim, levels = design)), trend = TRUE, robust = TRUE)
tB <- topTable(fitB, number = Inf)
truth_eval(rownames(tB)[tB$adj.P.Val < 0.05], truth, 'paired limma, >=2 complete donor pairs')
cat('rows kept: Skill filter', sum(keep_skill), '| >=2 pairs', sum(keep_pairs), '\n')
