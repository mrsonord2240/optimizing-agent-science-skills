# Input 3 (Edge) - bio-differential-expression-deseq2-basics
# padj = NA. The Skill names three distinct causes (independent filtering, Cook's outlier,
# all-zero in a group) with three different fixes. Each is constructed here on the real
# pseudobulk matrix and each prescribed fix is applied and measured.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({library(DESeq2); library(IHW)})

OUT <- 'F:/OpenScience/audits/bio-differential-expression-deseq2-basics'
pb <- readRDS(file.path(OUT, 'data', 'pseudobulk_cd14_mono.rds'))
counts <- pb$counts; coldata <- pb$coldata
set.seed(20260916)

# construct the three cases on top of the real matrix
cm <- counts
# (1) a low-count but perfectly consistent "master regulator": ~10 counts everywhere, 3x up
cm <- rbind(cm, MASTER_TF = c(rep(8L, 4), rep(24L, 4)))
# (2) a gene whose signal lives in ONE sample (Cook's outlier)
cm <- rbind(cm, ONE_SAMPLE_GENE = c(rep(50L, 4), 50L, 50L, 50L, 4000L))
# (3) a gene that is all-zero in the control group
cm <- rbind(cm, ZERO_IN_CONTROL = c(rep(0L, 4), rep(300L, 4)))
cat('matrix with three constructed cases:', nrow(cm), 'genes\n')

dds <- DESeqDataSetFromMatrix(cm, coldata, design = ~ condition)
dds$condition <- relevel(dds$condition, ref = 'control')
dds <- dds[rowSums(counts(dds)) >= 10, ]
dds <- DESeq(dds, quiet = TRUE)
res <- results(dds, name = 'condition_treated_vs_control', alpha = 0.05)
probes <- c('MASTER_TF', 'ONE_SAMPLE_GENE', 'ZERO_IN_CONTROL')
show <- function(r, label) {
  df <- as.data.frame(r[probes, c('baseMean', 'log2FoldChange', 'pvalue', 'padj')])
  cat('\n', label, '\n', sep = '')
  print(round(df, 5))
}
show(res, 'DEFAULT results()')
cat('  Cook\'s cutoff applies? minReplicatesForReplace default =',
    formals(DESeq)$minReplicatesForReplace, '; n per group = 4\n')
cat('  independent filtering threshold (baseMean):',
    round(metadata(res)$filterThreshold, 2), '\n')

cat('\n--- fix 1: results(independentFiltering = FALSE) ---')
show(results(dds, name = 'condition_treated_vs_control', independentFiltering = FALSE),
     'independentFiltering = FALSE')
cat('\n--- fix 2: results(cooksCutoff = FALSE) ---')
show(results(dds, name = 'condition_treated_vs_control', cooksCutoff = FALSE),
     'cooksCutoff = FALSE')
cat('\n--- fix 3: filterFun = ihw (the Skill says "often less aggressive on low-count genes") ---')
# TOOLS.md note 7: IHW segfaults at default nbins on this build; pin nbins <= 5
r_ihw <- try(results(dds, name = 'condition_treated_vs_control', filterFun = function(...)
  ihw(..., nbins = 4)), silent = TRUE)
if (inherits(r_ihw, 'try-error')) {
  cat('\nIHW FAILED:', as.character(r_ihw))
} else {
  show(r_ihw, 'filterFun = ihw (nbins = 4)')
  cat('  total padj<0.05, default filtering:', sum(res$padj < 0.05, na.rm = TRUE),
      '| IHW:', sum(r_ihw$padj < 0.05, na.rm = TRUE), '\n')
}

cat('\n--- how many NAs of each kind across the whole matrix? ---\n')
r_nf <- results(dds, name = 'condition_treated_vs_control', independentFiltering = FALSE)
r_nc <- results(dds, name = 'condition_treated_vs_control', cooksCutoff = FALSE)
cat('  padj NA with defaults           :', sum(is.na(res$padj)), '/', nrow(res), '\n')
cat('  padj NA without indep. filtering:', sum(is.na(r_nf$padj)), '\n')
cat('  pvalue NA with defaults (Cook\'s):', sum(is.na(res$pvalue)), '\n')
cat('  pvalue NA with cooksCutoff=FALSE:', sum(is.na(r_nc$pvalue)), '\n')
cat('  all-zero rows (never testable)  :', sum(rowSums(counts(dds)) == 0), '\n')
cat('DONE\n')
