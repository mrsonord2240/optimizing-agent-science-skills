# Check whether the available Cairo package can retain fractional-point MediaBox values.
suppressPackageStartupMessages(library(ggplot2))
out <- "F:/OpenScience/audits/bio-data-visualization-multipanel-figures/run/multipanel_fix_20260923/out_r"
p <- ggplot(data.frame(x = 1:3, y = 1:3), aes(x, y)) + geom_point() + theme_classic(base_size = 7)
Cairo::CairoPDF(file.path(out, "cairo_package.pdf"), width = 183 / 25.4, height = 140 / 25.4)
print(p)
dev.off()
cat("Cairo package precision test written\n")
