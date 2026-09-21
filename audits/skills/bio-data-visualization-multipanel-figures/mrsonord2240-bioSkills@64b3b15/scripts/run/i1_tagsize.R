source("F:/OpenScience/audits/bio-data-visualization-multipanel-figures/run/common.R")
df <- read.csv(file.path(DATA, "i1_df.csv"))
p1 <- ggplot(df, aes(x, y)) + geom_point() + theme_classic() + labs(title = "SCATTER")
p2 <- ggplot(df, aes(group, value)) + geom_boxplot() + theme_classic() + labs(title = "BOX")
for (sz in c(6, 10, 20)) {
  f <- (p1 + p2) + plot_annotation(tag_levels = 'a', theme = theme(plot.tag = element_text(face = 'bold', size = sz)))
  ggsave(file.path(OUT, sprintf("tag_%d.pdf", sz)), f, width = 180, height = 70, units = 'mm', device = cairo_pdf)
}
# same, but tag theme via & (applies to all subplots)
f <- (p1 + p2) + plot_annotation(tag_levels = 'a') & theme(plot.tag = element_text(face = 'bold', size = 6))
ggsave(file.path(OUT, "tag_amp6.pdf"), f, width = 180, height = 70, units = 'mm', device = cairo_pdf)
