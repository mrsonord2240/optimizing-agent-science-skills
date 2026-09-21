# Input 2 follow-up: which selectLab genes does EnhancedVolcano 1.24 actually label? one gene per threshold class.
suppressMessages({library(DESeq2); library(EnhancedVolcano); library(ggplot2)})
D <- "F:/OpenScience/audits/bio-data-visualization-volcano-and-ma-plots"
o <- readRDS(file.path(D, "data/airway_objs.rds")); res <- o$apeglm; sym <- o$sym
ok <- !is.na(sym[rownames(res)]) & !duplicated(sym[rownames(res)]) & !duplicated(sym[rownames(res)], fromLast = TRUE)
newn <- sym[rownames(res)][ok]; res <- res[ok, ]; rownames(res) <- newn
df <- as.data.frame(res)
both <- "DUSP1"; ponly <- "TP53"
fconly <- rownames(df)[which(!is.na(df$padj) & df$padj >= 0.05 & abs(df$log2FoldChange) > 1)][1]
neither <- c("GAPDH", "ACTB")
napadj <- rownames(df)[is.na(df$padj)][1:2]
cls <- c(both = both, p_only = ponly, fc_only = fconly, neither = neither, na_padj = napadj)
print(round(df[cls, c("baseMean","log2FoldChange","padj")], 4))
p <- EnhancedVolcano(res, lab = rownames(res), x = "log2FoldChange", y = "padj", pCutoff = 0.05, FCcutoff = 1, selectLab = cls, drawConnectors = TRUE, maxoverlapsConnectors = Inf)
b <- ggplot_build(p); ll <- which(sapply(p$layers, function(l) inherits(l$geom, "GeomTextRepel")))
drawn <- unique(unlist(lapply(ll, function(i) as.character(b$data[[i]]$label))))
cat("requested:", paste(cls, collapse=","), "\n"); cat("drawn    :", paste(drawn, collapse=","), "\n")
for (n in names(cls)) cat(sprintf("  %-8s %-10s labelled=%s\n", n, cls[[n]], cls[[n]] %in% drawn))
# label layer data selection rule in source

png(file.path(D, "figs/i2c_selectlab_nonpassing.png"), 1400, 1100, res = 180); print(EnhancedVolcano(res, lab = rownames(res), x = "log2FoldChange", y = "padj", pCutoff = 0.05, FCcutoff = 1, selectLab = c("DUSP1","TP53","GAPDH","ACTB"), drawConnectors = TRUE, maxoverlapsConnectors = Inf)); invisible(dev.off())
")

src <- deparse(body(EnhancedVolcano::EnhancedVolcano)); k <- grep("!is.na(lab)", src, fixed = TRUE); cat("source lines using !is.na(lab):", length(k), "
"); cat(head(src[k], 4), sep = "
")
