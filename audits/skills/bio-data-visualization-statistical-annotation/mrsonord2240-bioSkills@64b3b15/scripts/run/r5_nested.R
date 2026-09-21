suppressPackageStartupMessages({library(ggpubr); library(rstatix); library(dplyr); library(lme4)})
D <- "F:/OpenScience/audits/bio-data-visualization-statistical-annotation"
n <- read.csv(file.path(D, "data", "nested.csv"))
cat("naive cells wilcox p (ggpubr default two-group method):\n")
p <- ggboxplot(n, x="group", y="value") + stat_compare_means(); print(ggplot_build(p)$data[[2]]$label)
cat("truth naive wilcox:", wilcox.test(value~group, n)$p.value, "\n")
m <- lmer(value ~ group + (1 | subject_id), data = n); s <- summary(m); print(s$coefficients)
cat("has p-value column? ", "Pr(>|t|)" %in% colnames(s$coefficients), "\n")
cat("lmerTest available? ", requireNamespace("lmerTest", quietly=TRUE), " emmeans:", requireNamespace("emmeans", quietly=TRUE), " pbkrtest:", requireNamespace("pbkrtest", quietly=TRUE), "\n")
if (requireNamespace("emmeans", quietly=TRUE)) print(emmeans::emmeans(m, pairwise ~ group, adjust = "holm")$contrasts)
ag <- n %>% group_by(group, subject_id) %>% summarise(value = mean(value), .groups="drop")
cat("aggregated per-patient wilcox p:", wilcox.test(value~group, ag)$p.value, " welch:", t.test(value~group, ag)$p.value, "\n")
# what a naive annotated boxplot of cells looks like with p.signif
p2 <- ggboxplot(n, x="group", y="value", add="jitter") + stat_compare_means(comparisons=list(c("Ctl","Trt")), method="wilcox.test", label="p.signif")
print(ggplot_build(p2)$data[[3]]$annotation[1])
# ICC / design effect for the record
cat("variance components:\n"); print(VarCorr(m))
