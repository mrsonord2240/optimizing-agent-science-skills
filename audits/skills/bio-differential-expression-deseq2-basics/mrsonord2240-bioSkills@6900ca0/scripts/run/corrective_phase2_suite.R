# Corrective Phase 2 regression suite for bio-differential-expression-deseq2-basics.
# Usage: micromamba run -n deseq2-repair-20260923 Rscript corrective_phase2_suite.R
# All data are deterministic synthetic integer counts; this script changes no Skill source.
suppressPackageStartupMessages({
  library(DESeq2)
  library(apeglm)
  library(ashr)
  library(IHW)
  library(tximport)
})

cat('R=', R.version.string, '\n', sep = '')
for (p in c('DESeq2', 'apeglm', 'ashr', 'IHW', 'tximport')) {
  cat(p, '=', as.character(packageVersion(p)), '\n', sep = '')
}

assert_ok <- function(label, value) {
  if (!isTRUE(value)) stop('ASSERTION FAILED: ', label, call. = FALSE)
  cat('ASSERTION PASS: ', label, '\n', sep = '')
}

make_counts <- function(n_genes = 240, n_samples = 8, seed = 20260923) {
  set.seed(seed)
  m <- matrix(rnbinom(n_genes * n_samples, mu = 90, size = 12), nrow = n_genes,
              dimnames = list(paste0('g', seq_len(n_genes)), paste0('s', seq_len(n_samples))))
  m[seq_len(30), (n_samples / 2 + 1):n_samples] <-
    m[seq_len(30), (n_samples / 2 + 1):n_samples] * 4L
  storage.mode(m) <- 'integer'
  m
}

fit_condition <- function(count_mat, coldata, design = ~ condition) {
  dds <- DESeqDataSetFromMatrix(count_mat, coldata, design = design)
  dds$condition <- relevel(factor(dds$condition), ref = 'control')
  dds <- dds[rowSums(counts(dds)) >= 10, ]
  DESeq(dds, quiet = TRUE)
}

cat('\n=== INPUT 1: canonical explicit-contrast pseudobulk workflow ===\n')
counts1 <- make_counts()
cd1 <- data.frame(condition = factor(rep(c('control', 'treated'), each = 4)),
                  row.names = colnames(counts1))
dds1 <- fit_condition(counts1, cd1)
res1 <- results(dds1, name = 'condition_treated_vs_control', alpha = 0.05)
shr1 <- lfcShrink(dds1, coef = 'condition_treated_vs_control', res = res1, type = 'apeglm')
cat('calls=', sum(res1$padj < 0.05, na.rm = TRUE), ' of 30 planted genes\n', sep = '')
assert_ok('explicit coefficient present', 'condition_treated_vs_control' %in% resultsNames(dds1))
assert_ok('apeglm retains pvalue with res=res', isTRUE(all.equal(res1$pvalue, shr1$pvalue)))
assert_ok('apeglm retains padj with res=res', isTRUE(all.equal(res1$padj, shr1$padj)))

cat('\n=== INPUT 2: batch and paired designs ===\n')
counts2 <- make_counts(n_samples = 8, seed = 20260924)
cd2 <- data.frame(condition = factor(rep(c('control', 'treated'), each = 4)),
                  batch = factor(rep(c('A', 'B'), 4)),
                  row.names = colnames(counts2))
d_batch <- fit_condition(counts2, cd2, ~ batch + condition)
r_batch <- results(d_batch, name = 'condition_treated_vs_control')
d_reverse <- fit_condition(counts2, cd2, ~ condition + batch)
r_reverse <- results(d_reverse, name = 'condition_treated_vs_control')
assert_ok('named contrast is formula-order invariant', isTRUE(all.equal(r_batch$log2FoldChange, r_reverse$log2FoldChange)))
counts_pair <- make_counts(n_samples = 8, seed = 20260925)
cd_pair <- data.frame(condition = factor(rep(c('control', 'treated'), 4)),
                      donor = factor(rep(paste0('D', 1:4), each = 2)),
                      row.names = colnames(counts_pair))
d_pair <- fit_condition(counts_pair, cd_pair, ~ donor + condition)
r_pair <- results(d_pair, name = 'condition_treated_vs_control')
cat('batch calls=', sum(r_batch$padj < .05, na.rm = TRUE),
    '; paired calls=', sum(r_pair$padj < .05, na.rm = TRUE), '\n', sep = '')
assert_ok('paired coefficient is named', 'condition_treated_vs_control' %in% resultsNames(d_pair))

cat('\n=== INPUT 3: padj=NA causes and tximport route ===\n')
counts3 <- rbind(make_counts(seed = 20260926), ZERO_IN_CONTROL = c(rep(0L, 4), rep(250L, 4)),
                 ALL_ZERO = rep(0L, 8))
cd3 <- data.frame(condition = factor(rep(c('control', 'treated'), each = 4)), row.names = colnames(counts3))
d3 <- DESeqDataSetFromMatrix(counts3, cd3, design = ~ condition)
d3$condition <- relevel(d3$condition, 'control')
d3 <- DESeq(d3, quiet = TRUE)
r3 <- results(d3, name = 'condition_treated_vs_control')
r3_no_filter <- results(d3, name = 'condition_treated_vs_control', independentFiltering = FALSE)
r3_ihw <- results(d3, name = 'condition_treated_vs_control', filterFun = ihw)
assert_ok('group-zero gene remains testable', !is.na(r3['ZERO_IN_CONTROL', 'padj']))
assert_ok('all-zero gene has NA padj', is.na(r3['ALL_ZERO', 'padj']))
assert_ok('IHW returns a result table', inherits(r3_ihw, 'DESeqResults'))
txi <- list(counts = make_counts(n_genes = 40, n_samples = 8, seed = 20260927),
            abundance = matrix(1, 40, 8), length = matrix(1000, 40, 8),
            countsFromAbundance = 'no')
colnames(txi$abundance) <- colnames(txi$counts); colnames(txi$length) <- colnames(txi$counts)
rownames(txi$abundance) <- rownames(txi$counts); rownames(txi$length) <- rownames(txi$counts)
dtx <- DESeqDataSetFromTximport(txi, cd1, design = ~ condition)
assert_ok('tximport offset route constructs a DESeqDataSet', inherits(dtx, 'DESeqDataSet'))
cat('no-filter NA=', sum(is.na(r3_no_filter$padj)), '; IHW calls=', sum(r3_ihw$padj < .05, na.rm = TRUE), '\n', sep = '')

cat('\n=== INPUT 4: interaction, contrast, and shrinkage ===\n')
counts4 <- make_counts(n_samples = 8, seed = 20260928)
cd4 <- data.frame(condition = factor(rep(c('control', 'treated'), each = 4)),
                  sex = factor(rep(c('F', 'M'), each = 2, times = 2)), row.names = colnames(counts4))
d4 <- fit_condition(counts4, cd4, ~ sex + condition + sex:condition)
int_name <- tail(resultsNames(d4), 1)
male <- results(d4, contrast = list(c('condition_treated_vs_control', int_name)))
apeglm_error <- try(lfcShrink(d4, contrast = list(c('condition_treated_vs_control', int_name)), type = 'apeglm'), silent = TRUE)
ashr_male <- lfcShrink(d4, contrast = list(c('condition_treated_vs_control', int_name)), type = 'ashr')
cd4$group <- factor(paste(cd4$sex, cd4$condition, sep = '_'))
dg4 <- DESeqDataSetFromMatrix(counts4, cd4, design = ~ 0 + group)
dg4 <- DESeq(dg4, quiet = TRUE)
group_male <- results(dg4, contrast = c('group', 'M_treated', 'M_control'))
assert_ok('apeglm rejects arbitrary list contrast', inherits(apeglm_error, 'try-error'))
assert_ok('ashr accepts arbitrary list contrast', inherits(ashr_male, 'DESeqResults'))
assert_ok('combined-factor LFC agrees with summed contrast', cor(male$log2FoldChange, group_male$log2FoldChange, use = 'complete.obs') > .999)

cat('\n=== INPUT 5: four-level omnibus LRT ===\n')
counts5 <- make_counts(n_samples = 8, seed = 20260929)
cd5 <- data.frame(grp = factor(rep(c('A', 'B', 'C', 'D'), each = 2)), row.names = colnames(counts5))
d5 <- DESeqDataSetFromMatrix(counts5, cd5, design = ~ grp)
dlrt <- DESeq(d5, test = 'LRT', reduced = ~ 1, quiet = TRUE)
rlrt <- results(dlrt)
dwald <- DESeq(d5, quiet = TRUE)
last_name <- tail(resultsNames(dwald), 1)
rlast <- results(dwald, name = last_name)
assert_ok('LRT LFC is the last named Wald coefficient', isTRUE(all.equal(rlrt$log2FoldChange, rlast$log2FoldChange)))
assert_ok('LRT produces omnibus adjusted p-values', any(!is.na(rlrt$padj)))

cat('\n=== INPUT 6: single-cell pseudobulk boundary ===\n')
set.seed(20260930)
cell_counts <- matrix(rnbinom(120 * 80, mu = 30, size = 8), 120,
                      dimnames = list(paste0('cell_gene', 1:120), paste0('cell', 1:80)))
cell_donor <- rep(paste0('D', 1:8), each = 10)
cell_condition <- rep(rep(c('control', 'treated'), each = 4), each = 10)
pseudo <- sapply(paste0('D', 1:8), function(d) rowSums(cell_counts[, cell_donor == d, drop = FALSE]))
colnames(pseudo) <- paste0('D', 1:8)
cd6 <- data.frame(condition = factor(rep(c('control', 'treated'), each = 4)), row.names = colnames(pseudo))
d6 <- fit_condition(pseudo, cd6)
r6 <- results(d6, name = 'condition_treated_vs_control')
assert_ok('pseudobulk has one column per biological donor', ncol(pseudo) == length(unique(cell_donor)))
assert_ok('pseudobulk uses the requested named condition coefficient', 'condition_treated_vs_control' %in% resultsNames(d6))
cat('cells=', ncol(cell_counts), '; donors=', ncol(pseudo), '; null pseudobulk calls=', sum(r6$padj < .05, na.rm = TRUE), '\n', sep = '')

cat('\n=== INPUT 7: bare results and post-hoc LFC claim ===\n')
counts7 <- make_counts(n_samples = 8, seed = 20261001)
cd7 <- data.frame(condition = factor(rep(c('control', 'treated'), each = 4)),
                  batch = factor(rep(c('A', 'B'), 4)), row.names = colnames(counts7))
d7 <- fit_condition(counts7, cd7, ~ condition + batch)
bare <- results(d7)
named <- results(d7, name = 'condition_treated_vs_control', alpha = .05)
threshold <- results(d7, name = 'condition_treated_vs_control', lfcThreshold = 1, alpha = .05)
assert_ok('bare results differs from named condition result in a multifactor design', !isTRUE(all.equal(bare$log2FoldChange, named$log2FoldChange)))
assert_ok('lfcThreshold returns a DESeqResults table', inherits(threshold, 'DESeqResults'))
cat('bare coefficient=', tail(resultsNames(d7), 1), '; named calls=', sum(named$padj < .05, na.rm = TRUE),
    '; threshold calls=', sum(threshold$padj < .05, na.rm = TRUE), '\n', sep = '')

cat('\nALL CORRECTIVE INPUTS PASSED\n')
