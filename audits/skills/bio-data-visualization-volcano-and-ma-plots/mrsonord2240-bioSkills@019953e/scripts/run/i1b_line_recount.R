# Recount for input 1: which points above the drawn hline (y > -log10(0.05)) are NOT FDR-significant?
o <- readRDS("F:/OpenScience/audits/bio-data-visualization-volcano-and-ma-plots/data/airway_objs.rds"); r <- as.data.frame(o$apeglm)
y <- -log10(r$pvalue); above <- y > -log10(0.05)
cat("genes above the drawn line:", sum(above, na.rm = TRUE), "\n")
cat("  of which padj >= 0.05:", sum(above & !is.na(r$padj) & r$padj >= 0.05, na.rm = TRUE), " padj NA:", sum(above & is.na(r$padj), na.rm = TRUE),
    " padj < 0.05:", sum(above & !is.na(r$padj) & r$padj < 0.05, na.rm = TRUE), "\n")
cat("  padj<0.05 but |LFC|<=1 (grey by design):", sum(!is.na(r$padj) & r$padj < .05 & abs(r$log2FoldChange) <= 1), "\n")
cat("largest y among padj>=0.05 genes:", round(max(y[!is.na(r$padj) & r$padj >= 0.05], na.rm = TRUE), 2), " boundary -log10(max p with padj<0.05):", round(-log10(max(r$pvalue[!is.na(r$padj) & r$padj < .05])), 2), "\n")
