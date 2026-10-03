# Re-audit 2b: which count does 'a cap of 50 hid 49 significant genes' correspond to? Usage: r.sh r2b_cap50.R
suppressMessages(library(DESeq2))
dds <- readRDS("F:/OpenScience/audit-envs/data-visualization/public-data/derived/airway_dds_condition.rds")
res <- suppressMessages(lfcShrink(dds, coef = 'condition_treated_vs_control', type = 'apeglm')); y <- -log10(res$padj)
cat("genes with -log10(padj) > 50, any LFC:", sum(y > 50, na.rm = TRUE), "\n")
cat("  of which |LFC| > 1 (coloured Up/Down):", sum(y > 50 & abs(res$log2FoldChange) > 1, na.rm = TRUE), "\n")
cat("  of which |LFC| <= 1 (grey NS but padj<0.05):", sum(y > 50 & abs(res$log2FoldChange) <= 1, na.rm = TRUE), "\n")
cat("genes with -log10(padj) > 30: any", sum(y > 30, na.rm = TRUE), " coloured", sum(y > 30 & abs(res$log2FoldChange) > 1, na.rm = TRUE), "\n")
