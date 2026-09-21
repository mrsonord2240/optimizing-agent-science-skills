suppressPackageStartupMessages({library(ggpubr); library(rstatix); library(dplyr)})
D <- "F:/OpenScience/audits/bio-data-visualization-statistical-annotation"
bd <- read.csv(file.path(D, "data", "border.csv")); bd$group <- factor(bd$group)
p <- ggboxplot(bd, x="group", y="value", add="jitter") + geom_pwc(method="wilcox_test", p.adjust.method="holm", label="p.adj.signif")
g <- ggplot_build(p); print(names(g$data[[length(g$data)]])); print(g$data[[length(g$data)]][, intersect(c("label","x","xend","y"), names(g$data[[length(g$data)]]))])
ggsave(file.path(D, "figs", "r7_geom_pwc.png"), p, width=6, height=5, dpi=100)
# same with an explicit ggsignif-style route: geom_signif with p taken from the adjusted rstatix table (manual annotations)
st <- bd %>% pairwise_wilcox_test(value ~ group, p.adjust.method="holm"); print(st[, c("group1","group2","p","p.adj","p.adj.signif")])
