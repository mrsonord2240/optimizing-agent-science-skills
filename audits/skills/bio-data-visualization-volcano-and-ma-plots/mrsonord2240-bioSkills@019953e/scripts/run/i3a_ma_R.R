# Input 3a: SKILL.md block 04 (plotMA) VERBATIM on real airway apeglm results, plus CSV export for the Python block.
suppressMessages({library(DESeq2)})
D <- "F:/OpenScience/audits/bio-data-visualization-volcano-and-ma-plots"
o <- readRDS(file.path(D, "data/airway_objs.rds")); res_apeglm <- o$apeglm; res_raw <- o$raw
write.csv(as.data.frame(res_apeglm), file.path(D, "data/airway_apeglm.csv"))
write.csv(as.data.frame(res_raw), file.path(D, "data/airway_raw_mle.csv"))
png(file.path(D, "figs/i3a_plotMA_block04.png"), 1400, 1100, res = 200)
source(file.path(D, "run/blocks/skill_block04.R"))      # plotMA(res_apeglm, alpha = 0.05, ylim = c(-5, 5))
dev.off()
# numbers behind the plot
sig <- !is.na(res_apeglm$padj) & res_apeglm$padj < 0.05
cat("padj<0.05:", sum(sig), " of ", nrow(res_apeglm), "\n")
oob <- !is.na(res_apeglm$log2FoldChange) & abs(res_apeglm$log2FoldChange) > 5
cat("genes with |shrunken LFC|>5 (outside ylim=c(-5,5)):", sum(oob), "  (plotMA draws these as edge triangles; not dropped)\n")
lo <- res_raw$baseMean < 10 
cat(sprintf("baseMean<10: n=%d. |LFC|>2 fraction raw MLE=%.4f, apeglm=%.4f\n", sum(lo), mean(abs(res_raw$log2FoldChange[lo]) > 2, na.rm = TRUE), mean(abs(res_apeglm$log2FoldChange[lo]) > 2, na.rm = TRUE)))
cat(sprintf("baseMean>=1000: median |LFC| raw=%.4f apeglm=%.4f (shrinkage should barely touch well-estimated genes)\n",
    median(abs(res_raw$log2FoldChange[res_raw$baseMean >= 1000]), na.rm = TRUE), median(abs(res_apeglm$log2FoldChange[res_apeglm$baseMean >= 1000]), na.rm = TRUE)))
