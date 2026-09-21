# Follow-up to input 2: measure EnhancedVolcano NA handling by non-NA y, capture print-time warnings, and read the selectLab source.
suppressMessages({library(DESeq2); library(EnhancedVolcano); library(ggplot2)})
D <- "F:/OpenScience/audits/bio-data-visualization-volcano-and-ma-plots"
o <- readRDS(file.path(D, "data/airway_objs.rds")); res <- o$apeglm; sym <- o$sym
ok <- !is.na(sym[rownames(res)]) & !duplicated(sym[rownames(res)]) & !duplicated(sym[rownames(res)], fromLast = TRUE)
newn <- sym[rownames(res)][ok]; res <- res[ok, ]; rownames(res) <- newn
p <- EnhancedVolcano(res, lab = rownames(res), x = "log2FoldChange", y = "padj", pCutoff = 0.05, FCcutoff = 1, selectLab = c("TP53","MYC","BRCA1"))
b <- ggplot_build(p)
y <- b$data[[1]]$y
cat("layer1 rows:", length(y), " non-NA y:", sum(!is.na(y)), " res non-NA padj:", sum(!is.na(res$padj)), " NA padj:", sum(is.na(res$padj)), "\n")
w <- character(); png(file.path(D, "figs/i2b_ev_tmp.png"), 800, 600); withCallingHandlers(print(p), warning = function(x) { w <<- c(w, conditionMessage(x)); invokeRestart("muffleWarning") }); dev.off()
cat("print-time warnings:\n"); print(unique(w))
cat("PASS/FAIL: drawn points == non-NA padj rows ->", sum(!is.na(y)) == sum(!is.na(res$padj)), "\n")
# what does selectLab do in the source?
src <- deparse(body(EnhancedVolcano::EnhancedVolcano))
i <- grep("selectLab", src); cat("selectLab lines in source:", length(i), "
"); idx <- sort(unique(pmin(c(i, i+1), length(src)))); cat(src[idx], sep = "
")
# gene with NA padj in selectLab: is it labelled?
na_gene <- rownames(res)[is.na(res$padj) & res$baseMean > 1][1]; cat("NA-padj gene:", na_gene, "\n")
p2 <- EnhancedVolcano(res, lab = rownames(res), x = "log2FoldChange", y = "padj", selectLab = c(na_gene, "GAPDH"), pCutoff=.05, FCcutoff=1)
b2 <- ggplot_build(p2); ll <- which(sapply(p2$layers, function(l) inherits(l$geom, "GeomTextRepel")))
cat("labels drawn for selectLab=c(NA-padj gene, GAPDH):", paste(unique(unlist(lapply(ll, function(i) as.character(b2$data[[i]]$label)))), collapse=","), "\n")
cat("GAPDH:"); print(round(as.data.frame(res)["GAPDH", c("baseMean","log2FoldChange","padj")], 3))
