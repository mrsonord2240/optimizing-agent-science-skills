# Phase 2 audit input 6: execute representative runnable blocks from every code-bearing reference.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
library(DESeq2)
library(apeglm)
library(ashr)
library(tximport)
set.seed(20260923)

make_counts <- function(n_genes, n_samples) {
  matrix(rnbinom(n_genes * n_samples, mu = 80, size = 12), nrow = n_genes,
         dimnames = list(paste0('g', seq_len(n_genes)), paste0('s', seq_len(n_samples))))
}

# interaction-designs.md and lfc-shrinkage.md
counts_i <- make_counts(200, 8)
col_i <- data.frame(genotype = factor(rep(c('WT', 'KO'), each = 4)),
                    treatment = factor(rep(rep(c('vehicle', 'drug'), each = 2), 2)),
                    row.names = colnames(counts_i))
col_i$genotype <- relevel(col_i$genotype, ref = 'WT')
col_i$treatment <- relevel(col_i$treatment, ref = 'vehicle')
dds_i <- DESeqDataSetFromMatrix(counts_i, col_i, ~ genotype + treatment + genotype:treatment)
dds_i <- DESeq(dds_i, quiet = TRUE)
rn_i <- resultsNames(dds_i)
stopifnot('treatment_drug_vs_vehicle' %in% rn_i)
male_effect <- results(dds_i, contrast = list(c('treatment_drug_vs_vehicle', 'genotypeKO.treatmentdrug')))
shrunk_ashr <- lfcShrink(dds_i, contrast = list(c('treatment_drug_vs_vehicle', 'genotypeKO.treatmentdrug')),
                         res = male_effect, type = 'ashr', quiet = TRUE)
stopifnot(nrow(shrunk_ashr) == 200L)
cat('interaction + ashr contrast: PASS\n')

# lrt.md
counts_l <- make_counts(200, 9)
col_l <- data.frame(group = factor(rep(c('control', 'A', 'B'), each = 3)), row.names = colnames(counts_l))
dds_l <- DESeqDataSetFromMatrix(counts_l, col_l, ~ group)
dds_l <- DESeq(dds_l, test = 'LRT', reduced = ~ 1, quiet = TRUE)
res_l <- results(dds_l)
stopifnot(nrow(res_l) == 200L, any(!is.na(res_l$pvalue)))
cat('LRT omnibus: PASS; last coefficient=', tail(resultsNames(dds_l), 1), '\n')

# padj-na-remedies.md, size-factors.md and transforms.md
counts_q <- make_counts(200, 8)
counts_q[1, ] <- 0L
counts_q[2, 1:4] <- 0L
col_q <- data.frame(condition = factor(rep(c('control', 'treated'), each = 4)), row.names = colnames(counts_q))
dds_q <- DESeqDataSetFromMatrix(counts_q, col_q, ~ condition)
dds_q <- estimateSizeFactors(dds_q, type = 'poscounts')
dds_q <- DESeq(dds_q, quiet = TRUE)
res_q <- results(dds_q)
stopifnot(is.na(res_q['g1', 'padj']), !is.na(res_q['g2', 'padj']))
vsd <- vst(dds_q, blind = FALSE, nsub = 100)
stopifnot(nrow(vsd) == 200L)
cat('all-zero / group-zero, poscounts, VST: PASS\n')

# tximport.md with four minimal Salmon-compatible quant files.
td <- file.path(tempdir(), 'p2_tximport')
dir.create(td, showWarnings = FALSE)
tx <- paste0('tx', 1:4)
for (i in 1:4) {
  delta <- if (i > 2) c(30, -20, 15, -10) else c(0, 0, 0, 0)
  q <- data.frame(Name = tx, Length = c(1000, 900, 800, 700), EffectiveLength = c(800, 700, 600, 500),
                  TPM = c(40, 30, 20, 10) + delta / 6, NumReads = c(100, 80, 60, 40) + delta)
  write.table(q, file.path(td, paste0('s', i, '.sf')), sep = '\t', row.names = FALSE, quote = FALSE)
}
files <- setNames(file.path(td, paste0('s', 1:4, '.sf')), paste0('s', 1:4))
tx2gene <- data.frame(TXNAME = tx, GENEID = c('geneA', 'geneA', 'geneB', 'geneB'))
txi <- tximport(files, type = 'salmon', tx2gene = tx2gene)
samples <- data.frame(condition = factor(rep(c('control', 'treated'), each = 2)), row.names = names(files))
dds_txi <- DESeqDataSetFromTximport(txi, colData = samples, design = ~ condition)
stopifnot(nrow(dds_txi) == 2L, ncol(dds_txi) == 4L)
cat('tximport -> DESeqDataSetFromTximport: PASS\n')
