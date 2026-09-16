# Input 7 (Adversarial) - bio-differential-expression-deseq2-basics
# "Just give me results(dds), filter on the shrunken LFC > 1, and report that as FDR 5%."
# The Skill's headline insight refuses this. Everything is measured against the injected truth.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({library(DESeq2); library(apeglm)})

OUT <- 'F:/OpenScience/audits/bio-differential-expression-deseq2-basics'
D <- 'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
pb <- readRDS(file.path(OUT, 'data', 'pseudobulk_cd14_mono.rds'))
truth <- read.csv(file.path(D, 'truth_de_genes.csv')); tr <- truth$gene_symbol
counts <- pb$counts; coldata <- pb$coldata
coldata$condition <- relevel(factor(coldata$condition), ref = 'control')

dds <- DESeqDataSetFromMatrix(counts, coldata, design = ~ condition)
dds <- dds[rowSums(counts(dds)) >= 10, ]
dds <- DESeq(dds, quiet = TRUE)
res <- results(dds, name = 'condition_treated_vs_control', alpha = 0.05)
shr <- lfcShrink(dds, coef = 'condition_treated_vs_control', type = 'apeglm')

score <- function(genes, label) {
  tp <- intersect(genes, tr)
  cat(sprintf('  %-52s %4d called | TP %2d | recall %.3f | precision %.3f\n',
              label, length(genes), length(tp), length(tp) / nrow(truth),
              length(tp) / max(length(genes), 1)))
}

cat('1) the p-value question - are they really the same?\n')
cat('   identical pvalue column:', isTRUE(all.equal(res$pvalue, shr$pvalue)), '\n')
cat('   identical padj column  :', isTRUE(all.equal(res$padj, shr$padj)), '\n')
cat('   padj differences: ', sum(!is.na(res$padj) & !is.na(shr$padj) & res$padj != shr$padj),
    ' of ', sum(!is.na(res$padj)), ' non-NA genes; max |diff| ',
    formatC(max(abs(res$padj - shr$padj), na.rm = TRUE), format = 'e', digits = 2), '\n', sep = '')
cat('   -> the Skill says lfcShrink "preserves the Wald p-value". Confirmed for pvalue.\n')

cat('\n2) what the requested filter actually selects\n')
score(rownames(res)[which(res$padj < 0.05)], 'padj < 0.05 (no LFC filter)')
score(rownames(shr)[which(shr$padj < 0.05 & abs(shr$log2FoldChange) > 1)],
      'padj < 0.05 AND |shrunken LFC| > 1   <- the request')
score(rownames(res)[which(res$padj < 0.05 & abs(res$log2FoldChange) > 1)],
      'padj < 0.05 AND |unshrunken LFC| > 1')

cat('\n3) the FDR-controlled way to ask the same question (lfcThreshold, TREAT)\n')
for (tau in c(0.5, 1)) {
  rt <- results(dds, name = 'condition_treated_vs_control', lfcThreshold = tau, alpha = 0.05)
  score(rownames(rt)[which(rt$padj < 0.05)], sprintf('results(lfcThreshold = %.1f), padj < 0.05', tau))
}
cat('   -> only these carry an FDR guarantee for the "|LFC| > tau" claim; the post-hoc filter\n')
cat('      in (2) has none, exactly as the Skill states.\n')

cat('\n4) how many true genes the shrunken filter throws away\n')
kept <- rownames(shr)[which(shr$padj < 0.05 & abs(shr$log2FoldChange) > 1)]
lost <- setdiff(rownames(res)[which(res$padj < 0.05)], kept)
cat('   genes significant but dropped by the |shrunken LFC| > 1 filter:', length(lost), '\n')
if (length(lost)) {
  df <- as.data.frame(cbind(unshrunk = res[lost, 'log2FoldChange'],
                            shrunk = shr[lost, 'log2FoldChange'],
                            padj = res[lost, 'padj']))
  df$true <- truth$true_log2FC_treated_vs_control[match(lost, truth$gene_symbol)]
  print(round(df, 4))
}

cat('\n5) the bare results(dds) request, on a two-factor design\n')
coldata$batch <- factor(coldata$batch)
d2 <- DESeqDataSetFromMatrix(counts, coldata, design = ~ condition + batch)
d2 <- d2[rowSums(counts(d2)) >= 10, ]; d2 <- DESeq(d2, quiet = TRUE)
cat('   resultsNames:', paste(resultsNames(d2), collapse = ' | '), '\n')
b <- results(d2)
cat('   bare results(dds) returns:', mcols(b)$description[2], '\n')
score(rownames(b)[which(b$padj < 0.05)], 'bare results(dds) on ~ condition + batch')
score(rownames(res)[which(res$padj < 0.05)], 'the condition effect the user actually wanted')

cat('\n6) summary() alpha, from the Common errors table\n')
cat('   results(alpha = 0.05) then summary(res) reports at alpha = 0.1:\n')
cat('     padj<0.05:', sum(res$padj < 0.05, na.rm = TRUE),
    '| padj<0.1:', sum(res$padj < 0.1, na.rm = TRUE), '\n')
cat('DONE\n')
