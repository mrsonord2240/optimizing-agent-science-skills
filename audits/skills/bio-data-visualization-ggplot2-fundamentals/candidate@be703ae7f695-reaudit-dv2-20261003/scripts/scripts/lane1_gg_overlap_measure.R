# Usage: r.sh|r-gg35.sh tools/lane1_gg_overlap_measure.R <skilldir> <outdir>   -- drawn ggrepel label boxes via tools/lane1_gg_lib_overlap.R (staged copy of the reaudit lib).
# Copy of fix-dv2 scripts/measure.R; only the input (derived symbol CSV) and lib path differ.
a <- commandArgs(TRUE); skill <- a[1]; out <- a[2]; dir.create(out, FALSE, TRUE)
suppressMessages({library(ggplot2); library(ggrepel); library(patchwork); library(grid)})
cat("ggplot2", as.character(packageVersion("ggplot2")), "ggrepel", as.character(packageVersion("ggrepel")), "\n")
suppressMessages(source(file.path(skill, "scripts/publication_figures.R")))
source("F:/OpenScience/audit-envs/data-visualization/tools/lane1_gg_lib_overlap.R")
setwd(out)
raw <- read.csv("F:/OpenScience/audit-envs/data-visualization/public-data/derived/airway_dex_deseq2_results_symbol.csv")   # built by tools/make_airway_results_symbol.R
top10 <- raw$symbol[order(raw$padj)][1:10]; cat("top10 symbols:", paste(top10, collapse = " "), " max nchar", max(nchar(top10)), "\n")
set.seed(7); df <- data.frame(g = rep(c("A","B","C"), each = 20), v = c(rnorm(20), rnorm(20, 1), rnorm(20, 2)))
pc <- prcomp(mtcars[, -1], scale. = TRUE); ve <- 100 * pc$sdev^2 / sum(pc$sdev^2)
pdf_ <- data.frame(pc$x[, 1:2], cyl = factor(mtcars$cyl), am = factor(mtcars$am), var_explained = ve[1:2])
bp <- create_boxplot(df, "g", "v", "g"); pp <- create_pca_plot(pdf_, "cyl", "am")
row <- function(tag, plot, w, h) {
  b <- label_boxes(plot, w, h); o <- overlaps(b); x <- outside(b)
  cat(sprintf("%-34s %3.0f x %3.0f mm | labels drawn %2d | overlapping pairs %d | outside panel %d%s\n", tag, w, h, nrow(b), nrow(o), nrow(x),
      if (nrow(o)) paste0(" [", paste(sprintf("%s~%s(%.1fx%.1f)", o$a, o$b, o$ox_mm, o$oy_mm), collapse = "; "), "]") else "")); flush(stdout())
  ggsave(paste0(gsub("[^A-Za-z0-9]+", "_", tag), "_", w, "x", h, ".png"), plot, width = w, height = h, units = "mm", dpi = 200)
}
ve_ <- create_volcano(raw); vs <- create_volcano(raw, label_col = "symbol")
cat("default labels: Ensembl", sum(ve_$data$label != ""), " symbol", sum(vs$data$label != ""), "\n")
for (s in list(c(183,128), c(150,105), c(120,84), c(89,70))) row("standalone_ens_default", ve_, s[1], s[2])
for (s in list(c(183,128), c(120,84), c(89,70))) row("standalone_sym_default", vs, s[1], s[2])
m3e <- create_multi_panel(ve_, bp, pp); m4e <- create_multi_panel(ve_, bp, pp, bp)
m3s <- create_multi_panel(vs, bp, pp); m4s <- create_multi_panel(vs, bp, pp, bp)
for (s in list(c(183,120), c(183,150), c(120,110))) { row("multi3_ens_default", m3e, s[1], s[2]); row("multi4_ens_default", m4e, s[1], s[2]) }
for (s in list(c(183,120), c(183,150), c(120,110))) { row("multi3_sym_default", m3s, s[1], s[2]); row("multi4_sym_default", m4s, s[1], s[2]) }
cat("\n-- PCA contract\n")
w <- NULL; p <- withCallingHandlers(create_pca_plot(transform(pdf_, var_explained = var_explained/100), "cyl"), warning = function(x) {w <<- conditionMessage(x); invokeRestart("muffleWarning")})
cat("fraction input warning:", w, "| label", p$labels$x, "\n")
w <- NULL; p <- withCallingHandlers(create_pca_plot(pdf_, "cyl"), warning = function(x) {w <<- conditionMessage(x); invokeRestart("muffleWarning")})
cat("percent input warning:", if (is.null(w)) "none" else w, "| label", p$labels$x, p$labels$y, " expected", sprintf("PC1 (%s%%)", round(ve[1],1)), "\n")
