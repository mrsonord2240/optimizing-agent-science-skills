# Re-audit 2 (volcano-and-ma-plots): scripts/volcano_plot.R volcano_plot() with and without y_cap; every count compared with the results table.
# Usage: r.sh r2_volcano_fn.R <skilldir> <outdir>   (needs out/core/airway_shrunk_apeglm.csv from r1 or recomputes it)
a <- commandArgs(TRUE); skill <- a[1]; out <- a[2]; dir.create(out, FALSE, TRUE); setwd(out)
suppressMessages({library(DESeq2); library(ggplot2)})
ok <- TRUE
chk <- function(l, c) { ok <<- ok && isTRUE(c); cat(sprintf("[%s] %s\n", if (isTRUE(c)) "PASS" else "FAIL", l)) }
dds <- readRDS("F:/OpenScience/audit-envs/data-visualization/public-data/derived/airway_dds_condition.rds")
res <- suppressMessages(lfcShrink(dds, coef = 'condition_treated_vs_control', type = 'apeglm'))
suppressMessages(source(file.path(skill, "scripts/volcano_plot.R")))
tab_up <- sum(res$padj < .05 & res$log2FoldChange > 1, na.rm = TRUE); tab_dn <- sum(res$padj < .05 & res$log2FoldChange < -1, na.rm = TRUE)
nonNA <- sum(!is.na(res$padj)); cat("table non-NA padj", nonNA, " sig Up", tab_up, " Down", tab_dn, " total sig", tab_up + tab_dn, "\n")
UP <- "#D55E00"; DN <- "#0072B2"
msgs <- character()
run <- function(...) withCallingHandlers(volcano_plot(res, ...), message = function(m) { msgs <<- c(msgs, conditionMessage(m)); invokeRestart("muffleMessage") },
                                         warning = function(w) { msgs <<- c(msgs, paste("WARN:", conditionMessage(w))); invokeRestart("muffleWarning") })
# --- 1. default: no cap
p0 <- run(label_genes = c("TP53", "MYC", "BRCA1")); b0 <- ggplot_build(p0); d0 <- b0$data[[1]]
cat("messages:", paste(msgs, collapse = " | "), "\n")
chk("padj=NA count is reported by message", any(grepl(as.character(sum(is.na(res$padj))), msgs)))
chk(sprintf("no cap: points plotted %d == non-NA padj %d", nrow(d0), nonNA), nrow(d0) == nonNA)
chk("no cap: plotted Up/Down equal table", sum(toupper(d0$colour) == UP) == tab_up && sum(toupper(d0$colour) == DN) == tab_dn)
yl <- b0$data[[3]]$yintercept; chk("no cap: hline = -log10(0.05)", abs(yl + log10(0.05)) < 1e-9)
chk("no cap: y is -log10(padj), max = 131.4 as stated ('airway reaches 131')", abs(max(d0$y) - max(-log10(res$padj), na.rm = TRUE)) < 1e-9 && round(max(d0$y)) == 131)
chk("no cap: every coloured point is on/above the line and every grey point with padj>=0.05 is below it", all(d0$y[toupper(d0$colour) != "#999999"] >= yl - 1e-9) && all(d0$y[toupper(d0$colour) == "#999999" & abs(d0$x) > 1] < yl + 1e-9))
lab0 <- b0$data[[4]]$label; chk(sprintf("labels drawn include TP53/MYC/BRCA1 (%s)", paste(lab0[lab0 != ""], collapse = ",")), all(c("TP53", "MYC", "BRCA1") %in% lab0))
# --- 2. cap 30
msgs <- character(); p30 <- run(y_cap = 30); b30 <- ggplot_build(p30); d30 <- b30$data[[1]]
tri <- d30$shape == 17; cat("cap 30: triangles", sum(tri), " significant among them", sum(tri & toupper(d30$colour) != "#999999"), "\n")
chk("cap 30: all genes still plotted (none dropped)", nrow(d30) == nonNA)
chk("cap 30: Up/Down counts unchanged vs table", sum(toupper(d30$colour) == UP) == tab_up && sum(toupper(d30$colour) == DN) == tab_dn)
chk("cap 30: max plotted y == 30 and capped genes are exactly those with -log10(padj) > 30", max(d30$y) == 30 && sum(tri) == sum(-log10(res$padj) > 30, na.rm = TRUE))
chk("cap 30: stated '118 triangles, 115 significant'", sum(tri) == 118 && sum(tri & toupper(d30$colour) != "#999999") == 115)
chk("cap 30: legend keeps a 'capped at 30' entry", any(grepl("capped at 30", unlist(lapply(b30$plot$scales$scales, function(s) s$labels)))))
chk("cap 30: hline still equals -log10(fdr)", abs(b30$data[[3]]$yintercept + log10(0.05)) < 1e-9)
ggsave("volcano_cap30.png", p30, width = 89, height = 90, units = "mm", dpi = 250)
ggsave("volcano_nocap.png", p0, width = 89, height = 90, units = "mm", dpi = 250)
# --- 3. old claim on coord_cartesian: cap 50 hides 49 significant genes
hid <- sum(-log10(res$padj) > 50 & (res$log2FoldChange > 1 | res$log2FoldChange < -1), na.rm = TRUE); cat("significant genes above y=50:", hid, "\n")
chk("claim 'clipping hid 49 significant genes at 50'", hid == 49)
# --- 4. label_genes absent -> warning
msgs <- character(); invisible(run(label_genes = c("TP53", "NOT_A_GENE"))); cat("absent-label messages:", paste(msgs, collapse = " | "), "\n")
chk("absent label gene produces a warning naming it", any(grepl("NOT_A_GENE", msgs)))
# --- 5. thresholds: stricter cutoffs keep the line equal to colour boundary
msgs <- character(); p01 <- run(fdr = 0.01, lfc_threshold = 1.5); b01 <- ggplot_build(p01); d01 <- b01$data[[1]]
chk("fdr=0.01: hline = -log10(0.01) and coloured points on/above it", abs(b01$data[[3]]$yintercept - 2) < 1e-9 && all(d01$y[toupper(d01$colour) != "#999999"] >= 2 - 1e-9))
chk("fdr=0.01, lfc=1.5: vlines at +-1.5", all(sort(b01$data[[2]]$xintercept) == c(-1.5, 1.5)))
exp_up <- sum(res$padj < .01 & res$log2FoldChange > 1.5, na.rm = TRUE); chk("fdr/lfc variant Up count equals table", sum(toupper(d01$colour) == UP) == exp_up)
# --- 6. data.frame input (no DESeqResults) with padj NA retained
df <- as.data.frame(res); df2 <- df[sample(nrow(df), 3000, FALSE), ]; set.seed(1)
msgs <- character(); pdf <- run_df <- withCallingHandlers(volcano_plot(df2), message = function(m) invokeRestart("muffleMessage")); chk("plain data.frame input works", inherits(pdf, "ggplot"))
# --- 7. ggbreak statement
suppressMessages(library(ggbreak)); pb <- p0 + scale_y_break(c(60, 100)); ggsave("volcano_ggbreak.png", pb, width = 89, height = 90, units = "mm", dpi = 150); chk("ggbreak scale_y_break draws on the volcano and saves", file.exists("volcano_ggbreak.png") && file.size("volcano_ggbreak.png") > 5000)
cat("RESULT", if (ok) "PASS" else "FAIL", "\n")
