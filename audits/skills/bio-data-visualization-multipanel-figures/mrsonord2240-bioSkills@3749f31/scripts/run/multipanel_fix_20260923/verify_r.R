# Verification for the multipanel correction. Run with data-visualization/r.sh.
suppressPackageStartupMessages({
  library(ggplot2)
  library(patchwork)
  library(cowplot)
  library(gridExtra)
})

out <- "F:/OpenScience/audits/bio-data-visualization-multipanel-figures/run/multipanel_fix_20260923/out_r"
dir.create(out, recursive = TRUE, showWarnings = FALSE)
old_wd <- getwd()
setwd(out)
on.exit(setwd(old_wd), add = TRUE)
# Some grob constructors can request R's default device while being evaluated.
# Hold a null PDF device so verification never leaves a spurious Rplots.pdf.
pdf(NULL)
on.exit(dev.off(), add = TRUE)

# Inputs 1 and 5: execute the shipped example in an audit-only cwd.
source("F:/OpenScience/wt/data-visualization-multipanel-figures/data-visualization/multipanel-figures/examples/multi_panel_figure.R")
stopifnot(file.exists("Figure1.pdf"), file.exists("Figure1.png"), file.info("Figure1.pdf")$size > 1000)

# Input 2: cowplot and gridExtra layout-matrix paths both render as documented.
set.seed(11)
d <- data.frame(x = rnorm(80), y = rnorm(80), group = rep(c("Control", "Treatment"), 40))
mk <- function(title) ggplot(d, aes(x, y, colour = group)) + geom_point() + labs(title = title) + theme_classic(base_size = 7)
p1 <- mk("one"); p2 <- mk("two"); p3 <- mk("three"); p4 <- mk("four")
cow <- plot_grid(p1, p2, p3, p4, ncol = 2, labels = "auto", label_size = 8,
                 label_fontface = "bold", align = "hv")
save_cairo_pdf <- function(path, plot, width_mm = 183, height_mm = 140) {
  Cairo::CairoPDF(path, width = width_mm / 25.4, height = height_mm / 25.4)
  on.exit(dev.off(), add = TRUE)
  if (inherits(plot, "grob")) grid::grid.draw(plot) else print(plot)
}
save_cairo_pdf("cowplot.pdf", cow)
layout <- rbind(c(1, 1, 2), c(3, 4, 4))
g <- invisible(arrangeGrob(p1, p2, p3, p4, layout_matrix = layout))
save_cairo_pdf("gridextra.pdf", g)
stopifnot(file.info("cowplot.pdf")$size > 1000, file.info("gridextra.pdf")$size > 1000)

# Input 4: tag styling requires `& theme()`, and flat wrap_plots accepts axis collection.
same_scale <- function(title) ggplot(d, aes(x, y, colour = group)) + geom_point() +
  scale_colour_manual(values = c(Control = "#4DBBD5", Treatment = "#E64B35"), name = "Condition") +
  coord_cartesian(xlim = c(-3, 3), ylim = c(-3, 3)) + labs(x = "X", y = "Y", title = title) + theme_classic(base_size = 7)
flat <- wrap_plots(lapply(letters[1:4], \(x) same_scale(x)), ncol = 2) +
  plot_layout(guides = "collect", axes = "collect", axis_titles = "collect") +
  plot_annotation(tag_levels = "a") &
  theme(plot.tag = element_text(size = 8, face = "bold"), plot.tag.location = "panel",
        plot.tag.position = c(0.02, 0.98), legend.position = "bottom")
save_cairo_pdf("flat_collect.pdf", flat)
stopifnot(file.info("flat_collect.pdf")$size > 1000)

cat("R verification PASS\n")
