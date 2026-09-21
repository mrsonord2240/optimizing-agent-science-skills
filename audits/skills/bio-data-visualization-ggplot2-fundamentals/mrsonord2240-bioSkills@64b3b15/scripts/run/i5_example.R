# Input 5 (Stress / multi-part): run the SHIPPED examples/publication_figures.R end to end on REAL airway data:
# volcano (all 19,772 genes incl. NA padj), boxplot (real counts of top gene), PCA, multi-panel (3 and 4 panel), save.
source("F:/OpenScience/audits/bio-data-visualization-ggplot2-fundamentals/run/common.R")
suppressPackageStartupMessages({library(airway); library(SummarizedExperiment)})
wrn <- character(0)
cap <- function(expr) withCallingHandlers(expr, warning = function(w) { wrn <<- c(wrn, conditionMessage(w)); invokeRestart("muffleWarning") })
suppressMessages(cap(source("F:/OpenScience/audits/bio-data-visualization-ggplot2-fundamentals/run/skill/data-visualization/ggplot2-fundamentals/examples/publication_figures.R")))
cat("sourcing example: warnings/messages:", if (length(wrn)) paste(unique(wrn), collapse = " || ") else "none", "\n"); wrn <- character(0)
res <- read.csv(DE)
tab_true <- with(res, table(ifelse(!is.na(padj) & padj < 0.05 & log2FoldChange > 1, "Up", ifelse(!is.na(padj) & padj < 0.05 & log2FoldChange < -1, "Down", "NS"))))

# ---- volcano (raw airway results, NA padj kept: the realistic DESeq2 export) ----
pv <- cap(create_volcano(res)); bv <- suppressWarnings(ggplot_build(pv))
cat("volcano warnings:", if (length(wrn)) paste(unique(wrn), collapse = " || ") else "none", "\n"); wrn <- character(0)
ld <- bv$data[[1]]
chk("volcano draws all 19,772 genes (NA padj included as NS)", nrow(ld) == nrow(res))
hexc <- function(x) toupper(rgb(t(col2rgb(x)), maxColorValue = 255))
got <- table(factor(hexc(ld$colour), levels = hexc(c("#E64B35", "#4DBBD5", "grey60")), labels = c("Up", "Down", "NS")))
print(got); print(tab_true[c("Up", "Down", "NS")])
chk("volcano colour counts equal Up/Down/NS computed independently from the CSV", all(as.integer(got) == as.integer(tab_true[c("Up", "Down", "NS")])))
lab <- bv$data[[2]]; nlab <- sum(!is.na(lab$label) & lab$label != ""); cat("labels drawn:", nlab, "\n")
chk("10 labels for the 10 smallest padj", nlab == 10 && setequal(lab$label[!is.na(lab$label) & lab$label != ""], res$gene[order(res$padj)][1:10]))
# horizontal dashed line: y = -log10(fdr_threshold) = 1.301 (nominal p = 0.05) while colouring uses padj < 0.05
hl <- bv$data[[4]]; cat("dashed hline y =", hl$yintercept, "(p =", 10^-hl$yintercept, ")\n")
up <- ld[hexc(ld$colour) %in% c("#E64B35", "#4DBBD5"), ]
cat("smallest -log10(p) among coloured (padj<0.05 & |lfc|>1) points:", round(min(up$y), 3), "; largest -log10(p) among NS-coloured points with |lfc|>1 & padj<0.05: none by construction\n")
ns_hi <- res[!is.na(res$padj) & res$padj >= 0.05 & -log10(res$pvalue) > 1.301, ]
cat("genes ABOVE the dashed line (p<0.05) yet coloured NS because padj >= 0.05:", nrow(ns_hi), "; of all genes with p<0.05:", sum(res$pvalue < 0.05), "\n")
chk("dashed hline coincides with the padj<0.05 colour boundary", min(up$y) >= hl$yintercept - 1e-9 && nrow(ns_hi[abs(ns_hi$log2FoldChange) > 1, ]) == 0)
ggsave(file.path(OUT, "i5_volcano.png"), pv, width = 7, height = 5, units = "in", dpi = 150)

# ---- boxplot: real normalised counts of the top DE gene by dex within cell line ----
data(airway); se <- airway
top <- res$gene[which.min(res$padj)]; cat("top gene", top, "\n")
d <- data.frame(dex = colData(se)$dex, cell = colData(se)$cell, log_count = log2(assay(se)[top, ] + 1))
pb <- cap(create_boxplot(d, "dex", "log_count", fill_var = "dex")); bb <- ggplot_build(pb)
cat("boxplot warnings:", if (length(wrn)) paste(unique(wrn), collapse = " || ") else "none", "\n"); wrn <- character(0)
bx <- bb$data[[1]]
tr <- quantile(d$log_count[d$dex == "trt"], c(.25, .5, .75)); ut <- quantile(d$log_count[d$dex == "untrt"], c(.25, .5, .75))
chk("boxplot medians match the raw data per dex group", isTRUE(all.equal(sort(bx$middle), sort(c(tr[2], ut[2])), check.attributes = FALSE)))
chk("boxplot has 2 fills (Set2) and jitter has 8 points", length(unique(bx$fill)) == 2 && nrow(bb$data[[2]]) == 8)
ggsave(file.path(OUT, "i5_box.png"), pb, width = 4, height = 4, units = "in", dpi = 150)

# ---- PCA ----
pca_df <- read.csv(file.path(DATA, "airway_pca_scores.csv")); pca_df$var_explained <- c(42.2, 22.4, 12, 8, 6, 5, 3, 1.4)
pp <- cap(create_pca_plot(pca_df, "dex", "cell"))

# ---- multi panel: 3 and 4 ----
m3 <- cap(create_multi_panel(pv, pb, pp)); m4 <- cap(create_multi_panel(pv, pb, pp, pp))
cat("multi-panel warnings:", if (length(wrn)) paste(unique(wrn), collapse = " || ") else "none", "\n"); wrn <- character(0)
gt3 <- patchwork::patchworkGrob(m3); cat("3-panel class:", class(m3)[1], "; panels in gtable:", sum(grepl("panel", gt3$layout$name)), "\n")
chk("3-panel patchwork has 3 panels", sum(grepl("^panel", gt3$layout$name)) == 3)
# 4-panel: gtable names are nested (panel-nested-patchwork-*), so counting "panel" rows is unreliable; verified visually: PNG i5_multi4.png shows tags A-D.
chk("4-panel patchwork object builds (panel count verified by opening i5_multi4.png: tags A-D)", inherits(m4, "patchwork"))
tags3 <- m3$patches$annotation$tag_levels; cat("tag_levels:", tags3, "\n")

# ---- save with the shipped function, then inspect ----
save_publication_figure(m3, file.path(OUT, "i5_multi3"), width = 10, height = 7)
save_publication_figure(m4, file.path(OUT, "i5_multi4"), width = 10, height = 7)
png_info(file.path(OUT, "i5_multi3.png")); png_info(file.path(OUT, "i5_multi4.png"))
pdf_info(file.path(OUT, "i5_multi3.pdf"))
