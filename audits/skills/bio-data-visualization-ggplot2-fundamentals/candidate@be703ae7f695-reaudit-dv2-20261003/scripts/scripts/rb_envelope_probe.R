# Envelope probe beyond the Skill's measured rows: other heights and other top-10 sets (same airway data, re-ranked), drawn-box overlap counts.
a <- commandArgs(TRUE); skill <- a[1]; out <- a[2]; dir.create(out, FALSE, TRUE)
suppressMessages({library(ggplot2); library(ggrepel); library(patchwork); library(grid)})
cat("ggplot2", as.character(packageVersion("ggplot2")), "ggrepel", as.character(packageVersion("ggrepel")), "\n")
suppressMessages(source(file.path(skill, "scripts/publication_figures.R")))
source("F:/OpenScience/audits/bio-data-visualization-ggplot2-fundamentals/reaudit-dv2-20261003/scripts/lane1_gg_lib_overlap.R"); setwd(out)
raw <- read.csv("F:/OpenScience/audit-envs/data-visualization/public-data/derived/airway_dex_deseq2_results_symbol.csv")
raw <- raw[!is.na(raw$padj) & !is.na(raw$symbol) & nzchar(raw$symbol), ]
set.seed(7); df <- data.frame(g = rep(c("A","B","C"), each = 20), v = c(rnorm(20), rnorm(20, 1), rnorm(20, 2)))
pc <- prcomp(mtcars[, -1], scale. = TRUE); ve <- 100 * pc$sdev^2 / sum(pc$sdev^2)
pdf_ <- data.frame(pc$x[, 1:2], cyl = factor(mtcars$cyl), am = factor(mtcars$am), var_explained = ve[1:2])
bp <- create_boxplot(df, "g", "v", "g"); pp <- create_pca_plot(pdf_, "cyl", "am")
row <- function(tag, plot, w, h) { b <- label_boxes(plot, w, h); o <- overlaps(b); x <- outside(b)
  cat(sprintf("%-30s %3.0f x %3.0f mm | labels %2d | overlap pairs %d | outside %d%s\n", tag, w, h, nrow(b), nrow(o), nrow(x), if (nrow(o)) paste0(" [", paste(sprintf("%s~%s", o$a, o$b), collapse = "; "), "]") else "")); flush(stdout())
  ggsave(paste0(gsub("[^A-Za-z0-9]+", "_", tag), "_", w, "x", h, ".png"), plot, width = w, height = h, units = "mm", dpi = 200) }
sets <- list(default = raw, up_only = within(raw, padj <- ifelse(log2FoldChange > 1, padj, 1)), maxlfc = within(raw, padj <- ifelse(padj < 0.05, 1e-10 * rank(-abs(log2FoldChange)), padj)))
for (nm in names(sets)) { r <- sets[[nm]]; v <- create_volcano(r, label_col = "symbol"); lab <- r$symbol[order(r$padj)][1:10]
  cat(sprintf("\n## %s top10: %s (labels drawn by default: %d)\n", nm, paste(lab, collapse = " "), sum(v$data$label != "")))
  for (s in list(c(89,70), c(89,55), c(89,89), c(120,84), c(183,128))) row(paste0("sym_", nm), v, s[1], s[2])
  m3 <- create_multi_panel(v, bp, pp); m4 <- create_multi_panel(v, bp, pp, bp)
  for (s in list(c(183,90), c(183,100), c(183,120), c(183,150), c(183,200))) { row(paste0("m3_sym_", nm), m3, s[1], s[2]); row(paste0("m4_sym_", nm), m4, s[1], s[2]) } }
# Ensembl default with different top-3
for (nm in c("up_only", "maxlfc")) { r <- sets[[nm]]; v <- create_volcano(r); cat(sprintf("\n## ens %s labels: %s\n", nm, paste(v$data$label[v$data$label != ""], collapse = " ")))
  for (s in list(c(183,128), c(120,84))) row(paste0("ens_", nm), v, s[1], s[2])
  m3 <- create_multi_panel(v, bp, pp); for (s in list(c(183,100), c(183,120))) row(paste0("m3_ens_", nm), m3, s[1], s[2]) }
