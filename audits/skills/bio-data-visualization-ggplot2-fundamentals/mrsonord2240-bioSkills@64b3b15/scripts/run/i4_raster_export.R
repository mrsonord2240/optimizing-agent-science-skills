# Input 4 (Edge): 50,000-point scatter, vector axes + raster points, cairo_pdf / PNG / TIFF export. REAL data: airway DESeq2 genes resampled? No:
# 19,772 real genes x (baseMean, log2FC) + 30,228 rows jittered copies would be fake, so use SYNTHETIC 50,000-point cloud (seed 7), labelled as such.
source("F:/OpenScience/audits/bio-data-visualization-ggplot2-fundamentals/run/common.R")
suppressPackageStartupMessages({library(ggrastr); library(ggtext)})
set.seed(7)
n <- 50000
df <- data.frame(x = rnorm(n), grp = sample(c("A", "B"), n, TRUE))
df$y <- 0.6 * df$x + rnorm(n, sd = 0.8) + ifelse(df$grp == "B", 0.5, 0)
cat("SYNTHETIC n =", n, "\n")
theme_pub <- theme_classic(base_size = 10) + theme(panel.grid = element_blank(), axis.text = element_text(color = 'black'),
   axis.ticks = element_line(color = 'black', linewidth = 0.3), axis.line = element_line(color = 'black', linewidth = 0.3))
wrn <- character(0)
cap <- function(expr) withCallingHandlers(expr, warning = function(w) { wrn <<- c(wrn, conditionMessage(w)); invokeRestart("muffleWarning") })

# (1) SKILL.md 'Common Geoms' claim: geom_point(..., rasterize = TRUE) is "ggplot2 3.5+ inline"
p_inline <- cap(ggplot(df, aes(x, y)) + geom_point(alpha = 0.7, size = 1, rasterize = TRUE) + theme_pub)
invisible(cap(ggplot_build(p_inline)))
cat("geom_point(rasterize = TRUE) warnings:", if (length(wrn)) paste(unique(wrn), collapse = " || ") else "none", "\n")
ggsave(file.path(OUT, "i4_inline.pdf"), p_inline, width = 89, height = 70, units = "mm", device = cairo_pdf)
inl <- pdf_info(file.path(OUT, "i4_inline.pdf"))
wrn <- character(0)

# (2) SKILL.md ggrastr recipe (rasterise + theme_pub + ggsave(device = cairo_pdf))
p_rast <- cap(ggplot(df, aes(x, y)) + rasterise(geom_point(alpha = 0.5), dpi = 300) + theme_pub)
ggsave(file.path(OUT, "i4_rasterise.pdf"), p_rast, width = 89, height = 70, units = "mm", device = cairo_pdf)
ras <- pdf_info(file.path(OUT, "i4_rasterise.pdf"))
cat("ggrastr warnings:", if (length(wrn)) paste(unique(wrn), collapse = " || ") else "none", "\n")
cat("file sizes  vector:", file.size(file.path(OUT, "i4_inline.pdf")), " rasterised:", file.size(file.path(OUT, "i4_rasterise.pdf")), "\n")
chk("rasterise: PDF holds >= 1 embedded image and is smaller than the all-vector PDF", file.size(file.path(OUT, "i4_rasterise.pdf")) < file.size(file.path(OUT, "i4_inline.pdf")) / 3)
# data intact in rasterised layer
b <- ggplot_build(p_rast); chk("rasterised layer still carries all 50,000 rows", nrow(b$data[[1]]) == n)

# (3) other export paths in SKILL.md
ggsave(file.path(OUT, "i4_fig.png"), p_rast, width = 89, height = 70, units = "mm", dpi = 300)
tiff_ok <- tryCatch({ ggsave(file.path(OUT, "i4_fig.tiff"), p_rast, width = 89, height = 70, units = "mm", dpi = 300, compression = "lzw"); "ok" }, error = function(e) conditionMessage(e), warning = function(w) paste("warning:", conditionMessage(w)))
cat("ggsave tiff compression='lzw':", tiff_ok, "\n")
tf <- file.path(OUT, "i4_fig.tiff"); cat("tiff size:", file.size(tf), "\n")
png_info(file.path(OUT, "i4_fig.png"))

# (4) the export order in the SKILL snippet: ggsave('out.pdf', device = cairo_pdf) with NO plot arg -> uses last_plot()
p_rast  # print so last_plot() is set
ggsave(file.path(OUT, "i4_lastplot.pdf"), device = cairo_pdf, width = 89, height = 70, units = "mm")
pdf_info(file.path(OUT, "i4_lastplot.pdf"))

# (5) SKILL: TIFF page via PIL: check compression tag and dpi
