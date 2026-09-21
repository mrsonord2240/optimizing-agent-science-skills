source("F:/OpenScience/audits/bio-data-visualization-multipanel-figures/run/common.R")
df <- read.csv(file.path(DATA, "i1_df.csv"))
p1 <- ggplot(df, aes(x, y)) + geom_point() + theme_classic() + labs(title = "SCATTER")
p2 <- ggplot(df, aes(group, value)) + geom_boxplot() + theme_classic() + labs(title = "BOX")
p3 <- ggplot(df, aes(x)) + geom_histogram(bins=30) + theme_classic() + labs(title = "HIST")
p4 <- ggplot(df, aes(x, y, color = group)) + geom_point() + theme_classic() + labs(title = "COLOR")
mk <- function(...) (p1 + p2) / (p3 + p4) + plot_annotation(tag_levels = 'a', theme = theme(plot.tag = element_text(face = 'bold', size = 10))) + plot_layout(...)
for (nmv in c("none", "collect")) {
  f <- if (nmv == "none") mk() else mk(guides='collect', axes='collect', axis_titles='collect')
  s <- leaf_summary(f)
  cat(nmv, ": panels", s$panels, " guide-box", s$guide, " tags", s$tags, " axis-l", s$axisl, " axis-b", s$axisb, " xlab", s$xlab, " ylab", s$ylab, "\n")
  print(table(sub("[-.][0-9]+.*$", "", s$names)))
}
