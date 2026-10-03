# Core smoke: SKILL.md and reference snippets run as written; failure-modes claims.
# Usage: r.sh|r-gg35.sh r3_snippets.R <skilldir> <outdir>
a <- commandArgs(TRUE); skill <- a[1]; out <- a[2]; dir.create(out, FALSE, TRUE)
suppressMessages({library(ggplot2); library(ggrepel); library(patchwork); library(grid)})
cat("ggplot2", as.character(packageVersion("ggplot2")), "\n")
chk <- function(l, c) cat(sprintf("[%s] %s\n", if (isTRUE(c)) "PASS" else "FAIL", l))
setwd(skill); suppressMessages(source("scripts/publication_figures.R")); setwd(out)
W <- character(0); hw <- function(w) { W <<- c(W, conditionMessage(w)); invokeRestart("muffleWarning") }
raw <- read.csv("F:/OpenScience/audit-envs/data-visualization/public-data/differential-expression/airway_dex_deseq2_results.csv")
raw <- raw[!is.na(raw$padj), ]

cat("\n== Grammar in Layers block (verbatim)\n")
set.seed(3); df <- data.frame(condition = rep(c("ctrl", "trt"), each = 30), tissue = rep(c("liver", "brain", "lung"), 20), expression = exp(rnorm(60, 2)))
colnames(df)
g <- withCallingHandlers({
  ggplot(df, aes(x = condition, y = expression)) +
    geom_boxplot(outlier.shape = NA) +
    geom_jitter(aes(color = condition), width = 0.2, alpha = 0.5) +
    scale_y_continuous(transform = 'log10', breaks = scales::breaks_log(), labels = scales::label_number()) +
    scale_color_manual(values = c('#0072B2', '#D55E00')) +
    labs(x = NULL, y = 'Expression', title = 'Gene X across conditions', caption = 'Source: ...') +
    facet_wrap(~ tissue, ncol = 3, scales = 'free_y') +
    theme_classic(base_size = 10) +
    theme(strip.background = element_blank(), strip.text = element_text(face = 'bold'))
}, warning = hw)
b <- withCallingHandlers(ggplot_build(g), warning = hw)
for (i in 1:3) cat("panel", i, "y labels:", paste(b$layout$panel_params[[i]]$y$get_labels(), collapse = " "), "\n")
cat("warnings:", paste(unique(W), collapse = " | "), "\n")
chk("jitter colours are exactly the two palette entries", setequal(toupper(unique(b$data[[2]]$colour)), c("#0072B2", "#D55E00")))
ggsave("grammar_block.png", g, width = 183, height = 70, units = "mm", dpi = 200)

cat("\n== Theme snippet\n")
q <- ggplot(pdf_ <- data.frame(PC1 = mtcars$wt, PC2 = mtcars$mpg, group = factor(mtcars$am)), aes(PC1, PC2, color = group)) + geom_point() +
  scale_color_manual(values = okabe_ito[1:2]) + theme_publication()
ggsave("theme_snip.png", q, width = 89, height = 70, units = "mm", dpi = 200)
chk("theme snippet points use #0072B2/#D55E00", setequal(toupper(unique(ggplot_build(q)$data[[1]]$colour)), c("#0072B2", "#D55E00")))

cat("\n== Tidy evaluation\n")
plot_var <- function(df, x_var, y_var) ggplot(df, aes(x = .data[[x_var]], y = .data[[y_var]])) + geom_point()
plot_var2 <- function(df, x_var, y_var) ggplot(df, aes(x = {{ x_var }}, y = {{ y_var }})) + geom_point()
chk(".data[[var]] maps mtcars$wt", identical(ggplot_build(plot_var(mtcars, "wt", "mpg"))$data[[1]]$x, mtcars$wt))
chk("{{ }} with bare names maps mtcars$wt", identical(ggplot_build(plot_var2(mtcars, wt, mpg))$data[[1]]$x, mtcars$wt))
w2 <- ggplot_build(plot_var2(mtcars, "wt", "mpg"))$data[[1]]
chk("{{ }} with strings maps a constant (one unique x), as the Skill warns", length(unique(w2$x)) == 1)
W <- character(0); invisible(withCallingHandlers(ggplot_build(ggplot(mtcars, aes_string(x = "wt", y = "mpg")) + geom_point()), warning = hw))
cat("aes_string warning:", paste(unique(W), collapse = " | "), "\n")

cat("\n== ggtext snippet\n")
suppressMessages(library(ggtext))
gt <- ggplot(mtcars, aes(wt, mpg)) + geom_point() +
  labs(x = 'log<sub>2</sub> fold change', y = '\u2212log<sub>10</sub>(*p*)') +
  theme(axis.title.x = element_markdown(), axis.title.y = element_markdown())
ggsave("ggtext.png", gt, width = 89, height = 70, units = "mm", dpi = 300); cat("ggtext snippet rendered\n")
ggsave("ggtext.pdf", gt, width = 89, height = 70, units = "mm", device = cairo_pdf)

cat("\n== Saving block (cairo_pdf, ggrastr, PNG, TIFF)\n")
library(ggrastr)
big <- ggplot(raw, aes(log2FoldChange, -log10(padj))) + rasterise(geom_point(alpha = 0.5), dpi = 300) + theme_publication()
ggsave("figure.pdf", plot = big, width = 89, height = 70, units = "mm", device = cairo_pdf)
ggsave("figure.png", big, width = 89, height = 70, units = "mm", dpi = 300)
ggsave("figure.tiff", big, width = 89, height = 70, units = "mm", dpi = 300, compression = "lzw")
cat("png px", paste(dim(png::readPNG("figure.png"))[2:1], collapse = "x"), "\n")
ggsave("figure_defaultdev.pdf", big, width = 89, height = 70, units = "mm")
W <- character(0); invisible(withCallingHandlers(ggplot_build(ggplot(raw[1:100,], aes(log2FoldChange, -log10(padj))) + geom_point(rasterize = TRUE)), warning = hw))
cat("geom_point(rasterize=TRUE) conditions:", paste(unique(W), collapse = " | "), "\n")
cat("rasterized-pdf file size (KB) cairo vs all-vector: "); ggsave("allvec.pdf", ggplot(raw, aes(log2FoldChange, -log10(padj))) + geom_point(alpha = .5) + theme_publication(), width = 89, height = 70, units = "mm", device = cairo_pdf)
cat(round(file.size("figure.pdf")/1024), "vs", round(file.size("allvec.pdf")/1024), "\n")
ggsave("inches_trap.pdf", ggplot(mtcars, aes(wt, mpg)) + geom_point(), width = 89, height = 70, device = cairo_pdf, limitsize = FALSE)

cat("\n== failure-modes claims\n")
cl <- ggplot_build(ggplot(mtcars, aes(wt, mpg)) + geom_point(aes(color = 'red')))$data[[1]]$colour
cat("aes(color='red') colour:", unique(cl), "\n")
W <- character(0); invisible(withCallingHandlers(ggplot_build(ggplot(mtcars, aes(wt, mpg)) + geom_line(size = 0.5)), warning = hw)); cat("geom_line(size=) warning:", paste(unique(W), collapse = " | "), "\n")
# ggrepel default drop: dense labels with default max.overlaps
set.seed(1); dd <- data.frame(x = rnorm(60, sd = .05), y = rnorm(60, sd = .05), l = paste0("LABEL", 1:60))
W <- character(0); png("repel_default.png", 800, 600); withCallingHandlers(print(ggplot(dd, aes(x, y, label = l)) + geom_point() + geom_text_repel()), warning = hw, message = function(m) { W <<- c(W, conditionMessage(m)); invokeRestart("muffleMessage") }); dev.off()
cat("ggrepel default 60 clustered labels:", paste(unique(W), collapse = " | "), "\n")
