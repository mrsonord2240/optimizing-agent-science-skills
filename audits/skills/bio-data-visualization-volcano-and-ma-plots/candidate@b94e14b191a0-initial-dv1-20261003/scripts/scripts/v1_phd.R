# VOL audit run 1: shipped scripts/volcano_phd.R + volcano_plot.R on the real airway DESeq2 dataset, with independent assertions.
# Usage: r.sh v1_phd.R <skilldir> <outdir>
a <- commandArgs(TRUE); skill <- a[1]; out <- a[2]; dir.create(out, FALSE, TRUE); setwd(out)
suppressMessages({library(DESeq2)})
chk <- function(l, c) cat(sprintf("[%s] %s\n", if (isTRUE(c)) "PASS" else "FAIL", l))
dds <- readRDS("F:/OpenScience/audit-envs/data-visualization/public-data/derived/airway_dds_condition.rds")
cat("DESeq2", as.character(packageVersion("DESeq2")), " ggplot2", as.character(packageVersion("ggplot2")), " coef:", resultsNames(dds)[5], "\n")
cat("dds rows", nrow(dds), " rownames head:", paste(head(rownames(dds), 3), collapse=","), "\n")
W <- character(0)
suppressMessages(withCallingHandlers(source(file.path(skill, "scripts/volcano_phd.R"), echo = FALSE),
  warning = function(w) { W <<- c(W, conditionMessage(w)); invokeRestart("muffleWarning") }))
cat("warnings while sourcing volcano_phd.R:", paste(unique(substr(W, 1, 90)), collapse = " | "), "\n")
# ---- independent recomputation from the shrunken table
r <- as.data.frame(res)
up <- sum(r$padj < .05 & r$log2FoldChange > 1, na.rm = TRUE); dn <- sum(r$padj < .05 & r$log2FoldChange < -1, na.rm = TRUE)
cat("sig counts (script):", paste(names(table(res_df$significance)), table(res_df$significance), collapse = " "), " independent Up", up, "Down", dn, "\n")
chk("Up/Down counts equal independent recount", sum(res_df$significance == "Up") == up && sum(res_df$significance == "Down") == dn)
# ---- labels: genes_of_interest on Ensembl rownames
cat("TP53/MYC/BRCA1 present in rownames:", sum(genes_of_interest %in% res_df$gene), "of 3; labelled genes:", paste(labels, collapse = ","), "\n")
chk("requested genes_of_interest appear in the labelled set (or the script says why not)", all(genes_of_interest %in% labels) && all(genes_of_interest %in% res_df$gene))
# ---- threshold line vs colour boundary
hy <- -log10(fdr); sg <- res_df[res_df$significance != "NS", ]
cat(sprintf("hline y = %.3f ; min -log10(p) among coloured = %.3f ; grey points above the line = %d (|LFC|>1 and above line but grey: %d)\n", hy, min(sg$neg_log10_p),
  sum(res_df$neg_log10_p > hy & res_df$significance == "NS", na.rm = TRUE),
  sum(res_df$neg_log10_p > hy & res_df$significance == "NS" & abs(res_df$log2FoldChange) > 1, na.rm = TRUE)))
chk("horizontal line coincides with the colour boundary (SKILL: 'threshold line matches the adjusted p threshold')", abs(hy - min(sg$neg_log10_p)) < 0.1)
# ---- y cap
n_cap <- sum(res_df$neg_log10_p > y_cap, na.rm = TRUE); cap_lab <- sum(res_df$label != "" & res_df$neg_log10_p > y_cap, na.rm = TRUE)
cat(sprintf("y_cap = %d: %d points above the cap (%d of them significant), %d of %d labelled genes lie above the cap; max -log10 p = %.1f\n", y_cap, n_cap, sum(res_df$significance[res_df$neg_log10_p > y_cap] != "NS", na.rm = TRUE), cap_lab, sum(res_df$label != ""), max(res_df$neg_log10_p, na.rm = TRUE)))
chk("no significant point is hidden by the y cap", sum(res_df$significance[res_df$neg_log10_p > y_cap] != "NS", na.rm = TRUE) == 0)
ggsave("volcano_phd_view.png", p_volcano, width = 89, height = 90, units = "mm", dpi = 200)
# ---- shrinkage claims
raw <- results(dds, name = resultsNames(dds)[5]); ix <- intersect(rownames(raw), rownames(res)); m <- raw[ix, ]; s <- res[ix, ]
ok <- is.finite(m$log2FoldChange) & is.finite(s$log2FoldChange)
bigger <- sum(abs(s$log2FoldChange[ok]) > abs(m$log2FoldChange[ok]) + 1e-8)
cat(sprintf("genes: %d; |shrunken| > |MLE| for %d; max |MLE| %.2f (%s) vs max |shrunken| %.2f (%s)\n", sum(ok), bigger, max(abs(m$log2FoldChange[ok])), ix[ok][which.max(abs(m$log2FoldChange[ok]))],
  max(abs(s$log2FoldChange[ok])), ix[ok][which.max(abs(s$log2FoldChange[ok]))]))
lowc <- ok & m$baseMean < 5; cat(sprintf("baseMean<5 genes: median |MLE| %.2f, median |shrunk| %.2f\n", median(abs(m$log2FoldChange[lowc])), median(abs(s$log2FoldChange[lowc]))))
chk("shrinkage never inflates an LFC (|shrunken| <= |MLE|)", bigger == 0)
chk("shrinkage pulls low-count genes toward zero", median(abs(s$log2FoldChange[lowc])) < median(abs(m$log2FoldChange[lowc])))
# ---- ashr contrast + svalue claim
res_ashr <- lfcShrink(dds, contrast = c("condition", "treated", "control"), type = "ashr")
cat("ashr result columns:", paste(colnames(res_ashr), collapse = ","), "\n")
chk("ashr result carries an svalue column (SKILL.md: 'ashr also returns svalue')", "svalue" %in% colnames(res_ashr))
res_sv <- lfcShrink(dds, coef = resultsNames(dds)[5], type = "apeglm", svalue = TRUE)
n_s <- sum(res_sv$svalue < 0.005, na.rm = TRUE); n_p <- sum(raw$padj < 0.05, na.rm = TRUE)
ov <- length(intersect(rownames(res_sv)[which(res_sv$svalue < 0.005)], rownames(raw)[which(raw$padj < 0.05)]))
cat(sprintf("apeglm svalue=TRUE columns: %s
", paste(colnames(res_sv), collapse = ",")))
cat(sprintf("s<0.005 -> %d genes; results() padj<0.05 -> %d genes; overlap %d (reference: 's < 0.005 corresponds approximately to padj < 0.05')
", n_s, n_p, ov))
r1 <- tryCatch(lfcShrink(dds, contrast = c("condition", "treated", "control"), type = "apeglm"), error = function(e) conditionMessage(e))
cat("apeglm with contrast= ->", if (is.character(r1)) substr(r1, 1, 80) else "accepted", "\n")
# ---- volcano_plot() function
source(file.path(skill, "scripts/volcano_plot.R"))
vp <- volcano_plot(res, label_genes = c("TP53", "MYC", "BRCA1")); b <- ggplot_build(vp)
cat("volcano_plot(label_genes=symbols on Ensembl rownames): labelled points =", sum(vp$data$label != ""), "(no warning)\n")
vp2 <- volcano_plot(res); ggsave("volcano_plot_fn.png", vp2, width = 89, height = 90, units = "mm", dpi = 200)
b2 <- ggplot_build(vp2); cat("volcano_plot() default: hline y =", round(-log10(0.05), 3), "; min coloured -log10p =", round(min(vp2$data$neg_log10_p[vp2$data$significance != "NS"]), 3), "; labels:", sum(vp2$data$label != ""), "\n")
# ---- EnhancedVolcano
ev <- EnhancedVolcano(res, lab = rownames(res), x = "log2FoldChange", y = "padj", pCutoff = fdr, FCcutoff = lfc_threshold,
  selectLab = labels, drawConnectors = TRUE, widthConnectors = 0.3, maxoverlapsConnectors = Inf, col = c("grey60", "#0072B2", "#56B4E9", "#D55E00"), pointSize = 1.5, labSize = 3, colAlpha = 0.6)
ggsave("enhancedvolcano_skill.png", ev, width = 7, height = 7, dpi = 100)
ed <- ev$data; col_by_dir <- table(ed$Sig[ed$padj < .05 & ed$log2FoldChange > 1], useNA = "no"); col_dn <- table(ed$Sig[ed$padj < .05 & ed$log2FoldChange < -1])
cat("EnhancedVolcano class of Up genes:", paste(names(col_by_dir), col_by_dir), "| of Down genes:", paste(names(col_dn), col_dn), "\n")
chk("EnhancedVolcano example colours Up and Down differently (SKILL: 'color by direction')", !identical(names(col_by_dir), names(col_dn)))
# selectLab gotcha: one gene passing thresholds, one failing, one absent
pass <- res_df$gene[res_df$significance == "Up"][1]; fail <- res_df$gene[res_df$significance == "NS" & !is.na(res_df$padj)][1]
ev2 <- EnhancedVolcano(res, lab = rownames(res), x = "log2FoldChange", y = "padj", pCutoff = fdr, FCcutoff = lfc_threshold, selectLab = c(pass, fail, "TP53"), drawConnectors = TRUE, maxoverlapsConnectors = Inf)
bd <- ggplot_build(ev2)$data; lab_txt <- unlist(lapply(bd, function(d) if ("label" %in% names(d)) d$label else NULL)); lab_txt <- lab_txt[!is.na(lab_txt) & lab_txt != ""]
cat("selectLab = [passing, failing-threshold, absent 'TP53'] -> labels drawn:", paste(unique(lab_txt), collapse = ","), "(pass =", pass, ", fail =", fail, ")\n")
chk("selectLab gene that fails the thresholds is silently unlabeled (Gotcha 1 as documented)", !(fail %in% lab_txt) && pass %in% lab_txt)
# ---- MA plot
png("plotMA.png", 600, 500); plotMA(res, alpha = 0.05, ylim = c(-5, 5)); dev.off()
mn <- res_df[res_df$baseMean < 5 & is.finite(res_df$log2FoldChange), ]; cat("MA: baseMean<5 genes", nrow(mn), "median |LFC| (shrunken)", round(median(abs(mn$log2FoldChange)), 3), "\n")
ggsave("ma_plot_view.png", p_ma, width = 89, height = 70, units = "mm", dpi = 200)
write.csv(data.frame(gene = rownames(res), as.data.frame(res)), "airway_shrunk_apeglm.csv", row.names = FALSE)
cat("PDF sizes:", paste(c("volcano.pdf", "ma_plot.pdf"), file.size(c("volcano.pdf", "ma_plot.pdf")), "B", collapse = "; "), "\n")
