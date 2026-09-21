library(DESeq2)
plotMA(res_apeglm, alpha = 0.05, ylim = c(-5, 5))
# alpha colors significant points; ylim clips for readability without losing the gene
