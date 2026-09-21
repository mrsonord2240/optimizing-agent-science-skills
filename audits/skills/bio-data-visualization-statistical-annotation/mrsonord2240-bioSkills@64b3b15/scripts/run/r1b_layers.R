suppressPackageStartupMessages({library(ggpubr); library(ggsignif); library(rstatix); library(dplyr)})
D <- "F:/OpenScience/audits/bio-data-visualization-statistical-annotation"
df <- read.csv(file.path(D, "data", "border.csv")); df$group <- factor(df$group)
prs <- combn(levels(df$group), 2, simplify = FALSE)
p1 <- ggboxplot(df, x='group', y='value', color='group', add='jitter', palette='npg') +
  stat_compare_means(method='wilcox.test', comparisons=prs, label='p.signif', p.adjust.method='holm', method.args=list(alternative='two.sided'))
b <- ggplot_build(p1)
for (i in seq_along(b$data)) { cat("layer", i, class(p1$layers[[i]]$geom)[1], "cols:", paste(names(b$data[[i]]), collapse=","), "\n") }
print(p1$layers[[length(p1$layers)]]$geom_params[c("annotations","textsize")] )
print(p1$layers[[length(p1$layers)]]$stat_params[c("test","p.adjust.method","test.args")])
print(b$data[[length(b$data)]])
