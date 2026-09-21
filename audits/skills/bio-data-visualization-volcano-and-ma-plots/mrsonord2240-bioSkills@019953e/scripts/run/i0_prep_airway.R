# Prepare shared inputs: DESeq2 on Bioconductor airway (REAL data, Himes 2014), shrunken + unshrunken results, symbols.
suppressMessages({library(DESeq2); library(airway); library(apeglm); library(ashr); library(org.Hs.eg.db)})
cat("versions: DESeq2", as.character(packageVersion("DESeq2")), "EnhancedVolcano", as.character(packageVersion("EnhancedVolcano")),
    "ggplot2", as.character(packageVersion("ggplot2")), "ggrepel", as.character(packageVersion("ggrepel")),
    "apeglm", as.character(packageVersion("apeglm")), "ashr", as.character(packageVersion("ashr")), "\n")
cat("lfcShrink formals$type: "); print(formals(lfcShrink)$type)
data(airway)
airway$condition <- factor(ifelse(airway$dex == "trt", "treated", "control"), levels = c("control", "treated"))
dds <- DESeqDataSet(airway, design = ~ cell + condition)
dds <- dds[rowSums(counts(dds)) > 0, ]
dds <- DESeq(dds)
cat("resultsNames:", resultsNames(dds), "\n")
res_raw <- results(dds, name = "condition_treated_vs_control")
res_apeglm <- lfcShrink(dds, coef = "condition_treated_vs_control", type = "apeglm")
res_apeglm_sv <- lfcShrink(dds, coef = "condition_treated_vs_control", type = "apeglm", svalue = TRUE)
res_ashr <- lfcShrink(dds, contrast = c("condition", "treated", "control"), type = "ashr")
res_normal <- suppressMessages(lfcShrink(dds, coef = "condition_treated_vs_control", type = "normal"))
cat("columns raw:    ", colnames(res_raw), "\n")
cat("columns apeglm: ", colnames(res_apeglm), "\n")
cat("columns apeglm svalue=TRUE: ", colnames(res_apeglm_sv), "\n")
cat("columns ashr:   ", colnames(res_ashr), "\n")
cat("columns normal: ", colnames(res_normal), "\n")
cat("has svalue in ashr result (Skill says 'ashr also returns svalue'): ", "svalue" %in% colnames(res_ashr), "\n")
cat("n genes:", nrow(res_raw), " padj NA:", sum(is.na(res_raw$padj)), " padj<0.05:", sum(res_raw$padj < 0.05, na.rm = TRUE), "\n")
cat("apeglm padj identical to raw padj: ", isTRUE(all.equal(res_apeglm$padj, res_raw$padj)), "\n")
cat("s<0.005 (apeglm svalue):", sum(res_apeglm_sv$svalue < 0.005, na.rm = TRUE), " vs padj<0.05:", sum(res_apeglm_sv$padj < 0.05, na.rm = TRUE), "\n")
sym <- mapIds(org.Hs.eg.db, keys = rownames(res_raw), keytype = "ENSEMBL", column = "SYMBOL", multiVals = "first")
cat("symbols mapped:", sum(!is.na(sym)), "of", length(sym), "\n")
saveRDS(list(dds = dds, raw = res_raw, apeglm = res_apeglm, apeglm_sv = res_apeglm_sv, ashr = res_ashr, normal = res_normal, sym = sym),
        "F:/OpenScience/audits/bio-data-visualization-volcano-and-ma-plots/data/airway_objs.rds")
# low-count inflation check: unshrunken vs shrunken among baseMean<5
lo <- res_raw$baseMean < 5
cat(sprintf("baseMean<5 genes: %d; max|LFC| raw = %.2f, apeglm = %.2f, ashr = %.2f, normal = %.2f\n", sum(lo),
    max(abs(res_raw$log2FoldChange[lo]), na.rm=TRUE), max(abs(res_apeglm$log2FoldChange[lo]), na.rm=TRUE),
    max(abs(res_ashr$log2FoldChange[lo]), na.rm=TRUE), max(abs(res_normal$log2FoldChange[lo]), na.rm=TRUE)))
# top genes by raw p
top <- head(order(res_raw$pvalue), 10); cat("top10 by p:", paste(sym[top], collapse=","), "\n")
