# Input 1: SKILL.md block 02 (volcano_plot) run VERBATIM on real airway apeglm-shrunken results.
suppressMessages({library(DESeq2); library(dplyr); library(ggplot2); library(ggrepel)})
D <- "F:/OpenScience/audits/bio-data-visualization-volcano-and-ma-plots"
source(file.path(D, "run/blocks/skill_block02.R"))   # defines volcano_plot() (also attaches ggplot2/ggrepel/dplyr)
o <- readRDS(file.path(D, "data/airway_objs.rds"))
res <- o$apeglm; sym <- o$sym
fails <- 0; chk <- function(name, ok, note="") { cat(sprintf("[%s] %s %s\n", if (ok) "PASS" else "FAIL", name, note)); if (!ok) fails <<- fails + 1 }

# --- Run A: default call, Ensembl rownames as-is
pA <- volcano_plot(res)
png(file.path(D, "figs/i1_volcanoA_default.png"), 1400, 1200, res = 200); print(pA); dev.off()
bA <- ggplot_build(pA)
pts <- bA$data[[1]]                       # geom_point layer
cat("points drawn:", nrow(pts), " (non-NA pvalue rows in res:", sum(!is.na(res$pvalue)), ")\n")
chk("point count == rows with non-NA pvalue", nrow(pts) == sum(!is.na(res$pvalue)))
# numbers behind the plot against the input table
df <- as.data.frame(res); df$gene <- rownames(df)
cls <- with(df, ifelse(is.na(padj), "NS", ifelse(padj < .05 & log2FoldChange > 1, "Up", ifelse(padj < .05 & log2FoldChange < -1, "Down", "NS"))))
cat("class counts (all rows, incl pvalue NA):"); print(table(cls))
plotcls <- pA$data$significance[!is.na(pA$data$neg_log10_p)]
cat("class counts among plotted:"); print(table(plotcls))
chk("Up count on plot == independent recompute", sum(plotcls == "Up") == sum(cls == "Up" & !is.na(df$pvalue)))
chk("Down count on plot == independent recompute", sum(plotcls == "Down") == sum(cls == "Down" & !is.na(df$pvalue)))
# y and x values are the shrunken lfc and -log10(pvalue)
ord <- order(pA$data$log2FoldChange); 
chk("x range equals shrunken LFC range", isTRUE(all.equal(range(pts$x), range(df$log2FoldChange[!is.na(df$pvalue)]))))
chk("y max equals -log10(min pvalue)", isTRUE(all.equal(max(pts$y), -log10(min(df$pvalue, na.rm = TRUE)))))
# threshold lines
hl <- Filter(function(d) "yintercept" %in% names(d), bA$data)[[1]]$yintercept
vl <- Filter(function(d) "xintercept" %in% names(d), bA$data)[[1]]$xintercept
cat("hline y =", hl, "; vline x =", vl, "\n")
chk("vlines at +-1", all(sort(vl) == c(-1, 1)))
chk("hline at -log10(0.05)=1.301 (raw p axis)", isTRUE(all.equal(hl, -log10(0.05))))
# does the drawn hline separate colored (padj-significant) from grey points? (the Skill's own 'raw p threshold on adjusted axis' failure mode)
sigY <- pA$data$neg_log10_p[pA$data$significance != "NS"]; nsY <- pA$data$neg_log10_p[pA$data$significance == "NS"]
cat(sprintf("colored (Up/Down) min y = %.2f ; grey points above the line: %d (of %d NS); colored below line: %d\n",
    min(sigY, na.rm = TRUE), sum(nsY > hl, na.rm = TRUE), length(nsY), sum(sigY < hl, na.rm = TRUE)))
chk("line separates colored from grey (no grey above line)", sum(nsY > hl, na.rm = TRUE) == 0, "<- Skill's own failure mode (Raw p threshold line on adjusted axis)")
# the p value that padj<0.05 actually corresponds to
pthr <- max(df$pvalue[!is.na(df$padj) & df$padj < .05], na.rm = TRUE)
cat(sprintf("largest raw p with padj<0.05 = %.4g -> -log10 = %.2f (vs drawn line 1.30)\n", pthr, -log10(pthr)))
# labels chosen
labs <- unique(pA$data$label[pA$data$label != ""]); cat("labelled (Ensembl):", paste(labs, collapse=","), "\n")
cat("labelled (symbols): ", paste(sym[labs], collapse=","), "\n")
chk("10 labels rendered", length(labs) == 10)
lab_data <- Filter(function(d) "label" %in% names(d) && "x" %in% names(d) && !"yintercept" %in% names(d), bA$data)
cat("text-repel layer rows with non-empty label:", sum(lab_data[[1]]$label != ""), "\n")
# baseMean of labelled genes (should not be low-count noise)
cat("baseMean of labelled genes:", paste(round(df[labs, "baseMean"]), collapse=","), "\n")
# housekeeping check: top by raw p vs top by rank score
chk("no housekeeping (GAPDH/ACTB/B2M) among labels", !any(sym[labs] %in% c("GAPDH","ACTB","B2M"), na.rm = TRUE))

# --- Run B: user supplies genes of interest as SYMBOLS -> must map rownames to symbols first (Skill gives no ID-mapping guidance)
res_s <- res; s <- sym[rownames(res)]; ok <- !is.na(s) & !duplicated(s) & !duplicated(s, fromLast = TRUE)
res_s <- res_s[ok, ]; rownames(res_s) <- s[ok]
goi <- c("DUSP1", "KLF15", "PER1", "TSC22D3", "FKBP5", "TP53")   # 5 canonical dex-responsive genes + TP53 (not DE)
pB <- volcano_plot(res_s, label_genes = goi)
png(file.path(D, "figs/i1_volcanoB_symbols.png"), 1400, 1200, res = 200); print(pB); dev.off()
labB <- unique(pB$data$label[pB$data$label != ""]); cat("Run B labelled:", paste(labB, collapse=","), "\n")
chk("all 6 requested labels present in data and labelled (TP53 is non-DE but still labelled by ggrepel path)", setequal(labB, goi[goi %in% rownames(res_s)]), paste("labelled:", paste(labB, collapse=",")))
gB <- as.data.frame(res_s)[goi, c("baseMean","log2FoldChange","padj")]; print(round(gB, 4))
cat("\nSUMMARY: fails =", fails, "\n")
