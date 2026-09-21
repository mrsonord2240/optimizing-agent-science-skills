# Input 3 (Variant B): programmatic plots with tidy evaluation, on a REAL PCA of the Bioconductor airway RNA-seq counts
source("F:/OpenScience/audits/bio-data-visualization-ggplot2-fundamentals/run/common.R")
suppressPackageStartupMessages({library(airway); library(SummarizedExperiment); library(rlang); library(patchwork)})
data(airway); cts <- assay(airway); keep <- rowSums(cts >= 10) >= 4
x <- log2(cts[keep, ] + 1); x <- x[apply(x, 1, var) > 0, ]
pc <- prcomp(t(x), scale. = FALSE); ve <- 100 * pc$sdev^2 / sum(pc$sdev^2)
df <- data.frame(pc$x[, 1:4], sample = colnames(x), dex = colData(airway)$dex, cell = colData(airway)$cell)
df$`my var` <- df$PC1        # column name with a space
cat("airway PCA on", nrow(x), "genes x", ncol(x), "samples; variance PC1/PC2 =", round(ve[1], 1), round(ve[2], 1), "\n")
write.csv(df, file.path(DATA, "airway_pca_scores.csv"), row.names = FALSE)

labs_of <- function(p) if (exists("get_labs", asNamespace("ggplot2"))) ggplot2::get_labs(p) else p$labels   # ggplot2 4.0 computes labels at build time
wrn <- character(0)
cap <- function(expr) withCallingHandlers(expr, warning = function(w) { wrn <<- c(wrn, conditionMessage(w)); invokeRestart("muffleWarning") })

# ---- SKILL.md blocks verbatim ----
plot_var <- function(df, x_var, y_var) {
    ggplot(df, aes(x = .data[[x_var]], y = .data[[y_var]])) +
        geom_point()
}
plot_var2 <- function(df, x_var, y_var) {
    ggplot(df, aes(x = {{ x_var }}, y = {{ y_var }})) +
        geom_point()
}
p1 <- cap(plot_var(df, 'PC1', 'PC2')); b1 <- ggplot_build(p1)$data[[1]]
chk("plot_var(df,'PC1','PC2'): 8 points, x = PC1 and y = PC2 exactly", nrow(b1) == 8 && all.equal(b1$x, df$PC1) == TRUE && all.equal(b1$y, df$PC2) == TRUE)
chk("plot_var axis titles are 'PC1' / 'PC2' (no '.data[[x_var]]' leak)", identical(unname(labs_of(p1)$x), "PC1") && identical(unname(labs_of(p1)$y), "PC2"))
cat("plot_var label text (4.0.3: p$labels is empty until build; get_labs() gives them):", labs_of(p1)$x, "|", labs_of(p1)$y, "| raw p$labels$x =", deparse(p1$labels$x), "\n")
p2 <- cap(plot_var2(df, PC1, PC2)); b2 <- ggplot_build(p2)$data[[1]]
chk("plot_var2(df, PC1, PC2) bare names give identical data", isTRUE(all.equal(b1[, c("x", "y")], b2[, c("x", "y")])))
cat("plot_var2 axis labels:", labs_of(p2)$x, "|", labs_of(p2)$y, "\n")
# Skill states the doc claim: '{{ }}' works when the caller passes BARE names.  What if an agent passes strings (as in plot_var)?
p2s <- cap(plot_var2(df, "PC1", "PC2")); b2s <- ggplot_build(p2s)
cat("plot_var2 called with STRINGS: x is", class(b2s$data[[1]]$x), " unique x:", unique(b2s$data[[1]]$x), " unique y:", unique(b2s$data[[1]]$y), "\n")
chk("plot_var2 with strings silently draws a constant column instead of erroring", length(unique(b2s$data[[1]]$y)) == 1)

# deprecated aes_string: what warning does this ggplot2 emit?
wrn <- character(0)
p3 <- cap(ggplot(df, aes_string(x = 'PC1', y = 'PC2')) + geom_point()); invisible(cap(ggplot_build(p3)))
cat("aes_string warning text:", paste(unique(wrn), collapse = " || "), "\n")
chk("aes_string still draws but warns (Skill: 'deprecated')", length(wrn) > 0 && nrow(ggplot_build(p3)$data[[1]]) == 8)

# !!sym() variant named in the Skill
sym_plot <- function(df, x_var, y_var) ggplot(df, aes(x = !!sym(x_var), y = !!sym(y_var))) + geom_point()
b4 <- ggplot_build(sym_plot(df, "PC1", "PC2"))$data[[1]]
chk("!!sym(var) variant identical", isTRUE(all.equal(b1[, c("x", "y")], b4[, c("x", "y")])))

# Edge: column with a space; missing column; numeric-as-string
b5 <- ggplot_build(plot_var(df, "my var", "PC2"))$data[[1]]
chk("column name with a space works through .data[[...]]", isTRUE(all.equal(b5$x, df$PC1)))
r <- tryCatch({ ggplot_build(plot_var(df, "PCX", "PC2")); "no error" }, error = function(e) conditionMessage(e))
cat("missing column PCX ->", gsub("\n", " ", r), "\n")
chk("missing column raises an error naming the column", grepl("PCX", r))

# ---- the example's PCA function on this data (example takes pca_df with var_explained column) ----
suppressMessages(source("F:/OpenScience/audits/bio-data-visualization-ggplot2-fundamentals/run/skill/data-visualization/ggplot2-fundamentals/examples/publication_figures.R"))
pdf_ <- df; pdf_$var_explained <- ve[1:8]
pp <- cap(create_pca_plot(pdf_, "dex", "cell"))
bp <- ggplot_build(pp)
ld <- bp$data[[1]]
chk("PCA plot: 8 points, colours match dex (4 trt / 4 untrt) via Set1", nrow(ld) == 8 && length(unique(ld$colour)) == 2 && all(table(ld$colour) == 4))
chk("PCA plot: colour follows dex, not cell (colour partitions == dex partitions)", all(tapply(ld$colour, df$dex, function(z) length(unique(z))) == 1))
chk("PCA plot: shapes follow cell (4 levels)", length(unique(ld$shape)) == 4)
cat("PCA axis labels:", pp$labels$x, "|", pp$labels$y, "\n")
chk("axis label uses variance from data (PC1 (NN.N%))", grepl(sprintf("PC1 \\(%.1f%%\\)", ve[1]), pp$labels$x))
# NB: Set1 has only 9 colours -> tested with 3 groups; and a 10-level colour var?
df10 <- data.frame(PC1 = rnorm(20), PC2 = rnorm(20), grp = factor(rep(letters[1:10], 2)), var_explained = c(10, 5))
w10 <- character(0); invisible(withCallingHandlers(ggplot_build(create_pca_plot(df10, "grp")), warning = function(w) { w10 <<- c(w10, conditionMessage(w)); invokeRestart("muffleWarning") }))
cat("10-level colour variable through create_pca_plot ->", paste(unique(w10), collapse = " || "), "\n")
ggsave(file.path(OUT, "i3_pca.png"), pp, width = 89, height = 70, units = "mm", dpi = 300)
ggsave(file.path(OUT, "i3_plotvar.png"), p1, width = 89, height = 70, units = "mm", dpi = 200)
png_info(file.path(OUT, "i3_pca.png"))
cat("warnings during blocks:", paste(unique(wrn), collapse = " || "), "\n")
