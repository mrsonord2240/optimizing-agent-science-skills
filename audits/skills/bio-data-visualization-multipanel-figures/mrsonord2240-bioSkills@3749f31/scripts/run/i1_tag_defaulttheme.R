source("F:/OpenScience/audits/bio-data-visualization-multipanel-figures/run/common.R")
df <- read.csv(file.path(DATA, "i1_df.csv"))
a <- ggplot(df, aes(x, y)) + geom_point(); b <- ggplot(df, aes(x)) + geom_histogram(bins = 20)   # default theme_grey, no theme_classic
for (sz in c(6, 20)) ggsave(file.path(OUT, sprintf("tagdef_%d.pdf", sz)), (a + b) + plot_annotation(tag_levels = "a", theme = theme(plot.tag = element_text(face = "bold", size = sz))), width = 180, height = 70, units = "mm", device = cairo_pdf)
