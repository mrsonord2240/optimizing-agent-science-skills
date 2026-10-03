# Re-audit 1 (volcano-and-ma-plots): run scripts/volcano_phd.R unmodified on the fitted airway dds, then measure.
# Usage: r.sh r1_core.R <skilldir> <outdir>
a <- commandArgs(TRUE); skill <- a[1]; out <- a[2]; dir.create(out, FALSE, TRUE); setwd(out)
suppressMessages({library(DESeq2); library(ggplot2)})
ok <- TRUE
chk <- function(l, c) { ok <<- ok && isTRUE(c); cat(sprintf("[%s] %s\n", if (isTRUE(c)) "PASS" else "FAIL", l)) }
dds <- readRDS("F:/OpenScience/audit-envs/data-visualization/public-data/derived/airway_dds_condition.rds")
cat("DESeq2", as.character(packageVersion("DESeq2")), " dds genes:", nrow(dds), " resultsNames:", paste(resultsNames(dds), collapse = ","), "\n")
# the script needs coefficient 'condition_treated_vs_control'
chk("coef condition_treated_vs_control exists in dds", 'condition_treated_vs_control' %in% resultsNames(dds))
png("ev_phd%02d.png", 900, 900, res = 110)
w <- character();
withCallingHandlers(
  source(file.path(skill, "scripts/volcano_phd.R"), echo = FALSE, print.eval = TRUE),
  warning = function(x) { w <<- c(w, conditionMessage(x)); invokeRestart("muffleWarning") })
invisible(dev.off())
cat("warnings from volcano_phd.R (unique, first 100 chars):\n"); print(unique(substr(w, 1, 100)))
cat("volcano_phd.R ran to the end. files:", paste(list.files(pattern = "pdf$|png$"), collapse = ", "), "\n")

# ---- table-level counts
n_all <- nrow(res); n_na <- sum(is.na(res$padj)); cat("res rows", n_all, " padj NA", n_na, " non-NA", n_all - n_na, "\n")
sig_up <- sum(res$padj < 0.05 & res$log2FoldChange > 1, na.rm = TRUE); sig_dn <- sum(res$padj < 0.05 & res$log2FoldChange < -1, na.rm = TRUE)
cat("table: Up", sig_up, " Down", sig_dn, " total", sig_up + sig_dn, "\n")

# ---- phd.R volcano object p_volcano: what is plotted?
b <- ggplot_build(p_volcano); d <- b$data[[1]]
cat("p_volcano points plotted:", nrow(d), " (non-NA padj:", n_all - n_na, ")\n")
chk("every non-NA-padj gene is plotted", nrow(d) == n_all - n_na)
up_col <- "#D55E00"; dn_col <- "#0072B2"
n_up_p <- sum(toupper(d$colour) == up_col); n_dn_p <- sum(toupper(d$colour) == dn_col)
cat("plotted Up", n_up_p, " Down", n_dn_p, "\n")
chk("plotted Up/Down counts equal table counts", n_up_p == sig_up && n_dn_p == sig_dn)
yint <- b$data[[3]]$yintercept; cat("hline yintercept:", yint, " -log10(0.05) =", -log10(0.05), "\n")
chk("hline equals -log10(fdr)", abs(yint - (-log10(0.05))) < 1e-9)
sigd <- d[toupper(d$colour) != "#999999", ]; nsd <- d[toupper(d$colour) == "#999999", ]
chk(sprintf("every coloured (Up/Down) point lies on/above the line (min y %.4f, n=%d)", min(sigd$y), nrow(sigd)), nrow(sigd) > 0 && min(sigd$y) >= yint - 1e-9)
chk(sprintf("every point above the line with |x|>1 is coloured Up/Down (n above line and |x|>1: %d)", sum(d$y > yint & abs(d$x) > 1)), all(toupper(d$colour[d$y > yint & abs(d$x) > 1]) != "#999999"))
chk(sprintf("every point below the line is NS (n below line: %d)", sum(d$y < yint)), sum(d$y < yint) > 0 && all(toupper(d$colour[d$y < yint]) == "#999999"))
cat("NS genes with padj<0.05 but |LFC|<=1:", sum(toupper(d$colour) == "#999999" & d$y >= yint), "; NS genes with |LFC|>1 and padj>=0.05:", sum(toupper(d$colour) == "#999999" & abs(d$x) > 1), "
")
chk("y plotted is -log10(padj)", isTRUE(all.equal(sort(d$y), sort(-log10(res$padj[!is.na(res$padj)])))))
cat("max y plotted (uncapped):", round(max(d$y), 2), "\n")
lab <- b$data[[4]]; cat("labels drawn:", sum(lab$label != ""), " e.g.", paste(head(lab$label[lab$label != ""], 13), collapse = ","), "\n")
cat("rownames sample:", paste(head(rownames(res), 3), collapse = ","), "  TP53/MYC/BRCA1 in rownames:", paste(c('TP53','MYC','BRCA1') %in% rownames(res), collapse = "/"), "\n")

# ---- PDFs
cat(sprintf("%-16s %8d B\n", c("volcano.pdf", "ma_plot.pdf"), file.size(c("volcano.pdf", "ma_plot.pdf"))), sep = "")

# ---- EnhancedVolcano object from the script: re-run its call (labels, colours)
ev_data <- EnhancedVolcano::EnhancedVolcano(ev_res, lab = rownames(ev_res), x = 'log2FoldChange', y = 'padj', pCutoff = fdr, FCcutoff = lfc_threshold,
    selectLab = labels, colCustom = ev_col, ylab = bquote(-log[10]~'adjusted'~italic(P)), title = NULL, subtitle = NULL, caption = NULL,
    drawConnectors = TRUE, widthConnectors = 0.3, maxoverlapsConnectors = Inf, pointSize = 1.5, labSize = 3, colAlpha = 0.6, legendPosition = 'right')
eb <- ggplot_build(ev_data)$data[[1]]
cat("EnhancedVolcano points:", nrow(eb), " distinct colours:", paste(sort(unique(toupper(eb$colour))), collapse = " "), "\n")
chk("EnhancedVolcano draws Up #D55E00 and Down #0072B2 (distinct)", all(c(up_col, dn_col) %in% toupper(eb$colour)))
chk("EnhancedVolcano colour counts equal Up/Down table counts", sum(toupper(eb$colour) == up_col) == sig_up && sum(toupper(eb$colour) == dn_col) == sig_dn)
ev_lab <- ggplot_build(ev_data)$data
cat("EnhancedVolcano y axis label:", deparse(ev_data$labels$y), "\n")
saveRDS(list(sig_up = sig_up, sig_dn = sig_dn), "counts.rds")
write.csv(data.frame(gene = rownames(res), as.data.frame(res)), "airway_shrunk_apeglm.csv", row.names = FALSE)
cat("RESULT", if (ok) "PASS" else "FAIL", "\n")
