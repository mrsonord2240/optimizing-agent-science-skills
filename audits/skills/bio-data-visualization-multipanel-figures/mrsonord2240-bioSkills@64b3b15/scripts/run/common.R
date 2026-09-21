# shared helpers, multipanel-figures audit 2026-09-20
suppressPackageStartupMessages({library(ggplot2); library(patchwork); library(cowplot); library(grid)})
RUN <- "F:/OpenScience/audits/bio-data-visualization-multipanel-figures/run"
OUT <- "F:/OpenScience/audits/bio-data-visualization-multipanel-figures/out"
DATA <- "F:/OpenScience/audits/bio-data-visualization-multipanel-figures/data"
dir.create(OUT, showWarnings = FALSE); dir.create(DATA, showWarnings = FALSE)
chk <- function(label, cond) { cat(sprintf("[%s] %s\n", if (isTRUE(cond)) "PASS" else "FAIL", label)); invisible(isTRUE(cond)) }
png_info <- function(f) {
  im <- png::readPNG(f); d <- dim(im)
  nonwhite <- mean(apply(im[,,1:3, drop=FALSE], c(1,2), function(v) any(v < 0.98)))
  cat(sprintf("PNG %s: %d bytes, %d x %d px, nonwhite %.3f\n", basename(f), file.size(f), d[2], d[1], nonwhite))
  invisible(list(w=d[2], h=d[1], nonwhite=nonwhite))
}
# synthetic RNA-seq-like data (seed fixed): 400 genes, 2 groups x 12 samples
set.seed(2026)
make_data <- function() {
  n <- 400
  de <- data.frame(gene = paste0("G", 1:n), log2FC = rnorm(n, 0, 1.6), baseMean = 10^runif(n, 0.5, 4))
  de$pvalue <- pmin(1, 2 * pnorm(-abs(de$log2FC) * sqrt(log10(de$baseMean)) * runif(n, 1.2, 3)))
  de$padj <- p.adjust(de$pvalue, "BH")
  de$status <- factor(ifelse(de$padj < 0.05 & de$log2FC > 1, "Up", ifelse(de$padj < 0.05 & de$log2FC < -1, "Down", "NS")), levels = c("Up", "Down", "NS"))
  pca <- data.frame(PC1 = c(rnorm(12, -2, .8), rnorm(12, 2, .8)), PC2 = rnorm(24), group = rep(c("Control", "Treatment"), each = 12))
  expr <- data.frame(gene = rep(paste0("Gene", 1:4), each = 24), group = rep(rep(c("Control", "Treatment"), each = 12), 4))
  expr$value <- rnorm(96, mean = rep(c(5, 8, 3, 6), each = 24) + ifelse(expr$group == "Treatment", 1.5, 0), sd = 0.7)
  list(de = de, pca = pca, expr = expr)
}
D <- make_data()
if (!file.exists(file.path(DATA, "de.csv"))) { write.csv(D$de, file.path(DATA, "de.csv"), row.names = FALSE); write.csv(D$pca, file.path(DATA, "pca.csv"), row.names = FALSE); write.csv(D$expr, file.path(DATA, "expr.csv"), row.names = FALSE) }
# recursive grob-name walker (patchwork nests gtables)
walk_names <- function(g) {
  out <- character(0)
  if (inherits(g, "gtable")) { for (k in g$grobs) out <- c(out, walk_names(k)) ; out <- c(out, g$name) }
  else if (inherits(g, "gTree")) { out <- c(out, g$name); for (k in g$children) out <- c(out, walk_names(k)) }
  else out <- c(out, g$name)
  out
}
count_kind <- function(nm, pat) sum(grepl(pat, nm))
leaf_summary <- function(fig) {
  g <- patchwork::patchworkGrob(fig); nm <- walk_names(g)
  list(names = nm, panels = count_kind(nm, "^panel"), guide = count_kind(nm, "^guide-box"), tags = count_kind(nm, "tag"),
       axisl = count_kind(nm, "^axis-l"), axisb = count_kind(nm, "^axis-b"), xlab = count_kind(nm, "^xlab"), ylab = count_kind(nm, "^ylab"))
}
