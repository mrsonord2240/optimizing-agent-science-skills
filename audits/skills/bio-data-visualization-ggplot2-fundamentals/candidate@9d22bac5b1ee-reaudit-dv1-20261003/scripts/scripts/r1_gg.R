# Independent re-audit run: shipped scripts/publication_figures.R + SKILL.md/reference snippets.
# Usage: r.sh|r-gg35.sh r1_gg.R <skilldir> <outdir>   (lib_overlap.R beside it)
a <- commandArgs(TRUE); skill <- a[1]; out <- a[2]; dir.create(out, FALSE, TRUE)
here <- dirname(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE)))
suppressMessages({library(ggplot2); library(ggrepel); library(patchwork); library(grid)})
cat("ggplot2", as.character(packageVersion("ggplot2")), " R", as.character(getRversion()), "\n")
chk <- function(l, c) cat(sprintf("[%s] %s\n", if (isTRUE(c)) "PASS" else "FAIL", l))
suppressMessages(source(file.path(skill, "scripts/publication_figures.R"))); source(file.path(here, "lib_overlap.R"))
setwd(out)
W <- character(0); hw <- function(w) { W <<- c(W, conditionMessage(w)); invokeRestart("muffleWarning") }
raw <- read.csv("F:/OpenScience/audit-envs/data-visualization/public-data/differential-expression/airway_dex_deseq2_results.csv")
cat("airway rows", nrow(raw), "padj NA", sum(is.na(raw$padj)), "\n")
lname <- function(p) sapply(p$layers, function(l) class(l$geom)[1])

## ---- GG-001
cat("\n== GG-001 volcano threshold vs colour boundary\n")
p <- withCallingHandlers(create_volcano(raw), warning = hw); bld <- withCallingHandlers(ggplot_build(p), warning = hw)
cat("build warnings:", length(W), paste(unique(W), collapse = " | "), "\n")
d <- p$data
ind <- with(raw[!is.na(raw$padj), ], c(Up = sum(padj < .05 & log2FoldChange > 1), Down = sum(padj < .05 & log2FoldChange < -1)))
tb <- table(d$significance)
chk(sprintf("class counts == independent (Up %d Down %d NS %d)", ind[["Up"]], ind[["Down"]], tb[["NS"]]), tb[["Up"]] == ind[["Up"]] && tb[["Down"]] == ind[["Down"]])
print(lname(p))
pt <- bld$data[[which(lname(p) == "GeomPoint")]]; hl <- bld$data[[which(lname(p) == "GeomHline")]]
chk("plotted y of every point == -log10(padj) computed independently from raw", isTRUE(all.equal(sort(pt$y), sort(-log10(raw$padj[!is.na(raw$padj)])))))
cat(sprintf("hline yintercept %.4f ; -log10(0.05) %.4f\n", hl$yintercept, -log10(0.05)))
col_sig <- pt$colour != "grey60"
min_col <- min(pt$y[col_sig]); max_grey_lfc <- max(pt$y[!col_sig & abs(pt$x) > 1])
cat(sprintf("min plotted y of coloured points %.4f ; max plotted y of grey points with |LFC|>1: %.4f\n", min_col, max_grey_lfc))
chk("hline == FDR cutoff on the plotted axis", abs(hl$yintercept - -log10(0.05)) < 1e-9)
chk("every coloured point on/above the line", min_col >= hl$yintercept)
chk("no grey |LFC|>1 point above the line", max_grey_lfc <= hl$yintercept)
cat("y title:", deparse(p$labels$y), "\n")
p01 <- create_volcano(raw, fdr_threshold = 0.01); b01 <- ggplot_build(p01)
chk("fdr_threshold=0.01 moves hline to 2", abs(b01$data[[which(lname(p01) == "GeomHline")]]$yintercept - 2) < 1e-9)

## ---- GG-002
cat("\n== GG-002 save_publication_figure\n")
pub <- create_volcano(raw, top_n = 3)
save_publication_figure(pub, "pub_default")
save_publication_figure(pub, "pub_183", width = 183, height = 120)
png_dim <- function(f) paste(dim(png::readPNG(f))[2:1], collapse = "x")
cat("pub_default.png px", png_dim("pub_default.png"), "(89x70 mm @300 dpi = 1051x827)\n")
cat("pub_183.png px", png_dim("pub_183.png"), "(183x120 mm @300 dpi = 2161x1417)\n")
ggsave("default_dev.pdf", pub, width = 89, height = 70, units = "mm")  # failure-modes claim: default pdf() does not embed

## ---- GG-003
cat("\n== GG-003 theme / palette\n")
th <- theme_publication(); base <- theme_classic(base_size = 10)
chk("theme_publication: panel.border blank, panel bg == theme_classic", inherits(th$panel.border, "element_blank") && identical(th$panel.background, base$panel.background))
chk("panel.grid blank", inherits(th$panel.grid, "element_blank"))
chk("axis line, ticks, text black", th$axis.line$colour == "black" && th$axis.ticks$colour == "black" && th$axis.text$colour == "black")
chk("strip: no background, bold text", inherits(th$strip.background, "element_blank") && th$strip.text$face == "bold")
chk("okabe_ito[1:2] == SKILL.md #0072B2/#D55E00; 8 unique", identical(okabe_ito[1:2], c("#0072B2", "#D55E00")) && length(unique(okabe_ito)) == 8)
set.seed(7); df <- data.frame(g = rep(c("A","B","C"), each = 20), v = c(rnorm(20), rnorm(20, 1), rnorm(20, 2)))
pb <- create_boxplot(df, "g", "v", "g")
pc <- prcomp(mtcars[, -1], scale. = TRUE); ve <- 100 * pc$sdev^2 / sum(pc$sdev^2)
pdf_ <- data.frame(pc$x[, 1:2], cyl = factor(mtcars$cyl), am = factor(mtcars$am), var_explained = ve[1:2])
pp <- create_pca_plot(pdf_, "cyl", "am")
for (nm in c("volcano", "boxplot", "pca")) {
  t <- ggplot2:::plot_theme(list(volcano = p, boxplot = pb, pca = pp)[[nm]])
  chk(sprintf("%s: panel.border blank, grid blank, axis line black", nm),
      inherits(t$panel.border, "element_blank") && inherits(t$panel.grid, "element_blank") && t$axis.line$colour == "black")
}
oi <- toupper(okabe_ito)
chk("volcano coloured classes drawn from Okabe-Ito", all(toupper(setdiff(unique(pt$colour), "grey60")) %in% oi))
chk("boxplot fills Okabe-Ito", all(toupper(unique(ggplot_build(pb)$data[[1]]$fill)) %in% oi))
chk("PCA colours Okabe-Ito", all(toupper(unique(ggplot_build(pp)$data[[1]]$colour)) %in% oi))
mp <- create_multi_panel(create_volcano(raw, top_n = 3), pb, pp)
chk("multi-panel: every sub-plot keeps borderless theme_publication", all(sapply(mp$patches$plots, function(q) inherits(ggplot2:::plot_theme(q)$panel.border, "element_blank"))) && inherits(ggplot2:::plot_theme(mp)$panel.border, "element_blank"))
cur <- getwd(); setwd(skill); ok <- try(suppressMessages(source("scripts/publication_figures.R")), silent = TRUE); setwd(cur)
chk("SKILL.md source('scripts/publication_figures.R') works with cwd = Skill dir", !inherits(ok, "try-error"))

## ---- helper behaviours
cat("\n== helper guards\n")
j1 <- ggplot_build(create_boxplot(df, "g", "v", "g"))$data[[2]]$x; j2 <- ggplot_build(create_boxplot(df, "g", "v", "g"))$data[[2]]$x
chk("boxplot jitter reproducible across builds", identical(j1, j2))
bx <- ggplot_build(pb)$data[[1]]; chk("boxplot medians == raw medians", isTRUE(all.equal(as.numeric(bx$middle), as.numeric(tapply(df$v, df$g, median)))))
chk("PCA axis labels == prcomp variance", pp$labels$x == sprintf("PC1 (%s%%)", round(ve[1], 1)) && pp$labels$y == sprintf("PC2 (%s%%)", round(ve[2], 1)))
r <- try(create_pca_plot(pdf_[, c("PC1", "PC2", "cyl")], "cyl"), silent = TRUE); cat("no var_explained ->", conditionMessage(attr(r, "condition")), "\n")
many <- cbind(pdf_, grp = factor(rep(letters[1:12], length.out = 32)))
r <- try(create_pca_plot(many, "grp"), silent = TRUE); cat("12 groups ->", conditionMessage(attr(r, "condition")), "\n")
frac <- pdf_; frac$var_explained <- frac$var_explained / 100
cat("fraction-valued var_explained label (contract is percent):", create_pca_plot(frac, "cyl")$labels$x, "\n")
r <- try(create_volcano(raw[, c("log2FoldChange", "gene")]), silent = TRUE); cat("volcano without padj ->", conditionMessage(attr(r, "condition")), "\n")
r <- try(ggplot_build(create_volcano(raw, label_col = "nope")), silent = TRUE); cat("volcano bad label_col ->", if (inherits(r, "try-error")) conditionMessage(attr(r, "condition")) else "ok", "\n")
