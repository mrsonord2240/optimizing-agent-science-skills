# SKILL.md ggpubr blocks verbatim on SYNTHETIC data; assert content of layers vs independent base-R computation
suppressPackageStartupMessages({library(ggpubr); library(ggsignif); library(rstatix); library(dplyr)})
cat("ggpubr", as.character(packageVersion("ggpubr")), "ggsignif", as.character(packageVersion("ggsignif")), "rstatix", as.character(packageVersion("rstatix")), "\n")
D <- "F:/OpenScience/audits/bio-data-visualization-statistical-annotation"
F <- file.path(D, "figs")
ex <- function(name, f) { r <- tryCatch(f(), error=function(e) {cat("ERROR in", name, ":", conditionMessage(e), "\n"); NULL}); r }

for (dset in c("three_group", "border")) {
  df <- read.csv(file.path(D, "data", paste0(dset, ".csv")))
  gl <- unique(df$group)
  df$group <- factor(df$group, levels = gl)
  prs <- combn(gl, 2, simplify = FALSE)
  raw <- sapply(prs, function(p) wilcox.test(df$value[df$group==p[1]], df$value[df$group==p[2]])$p.value)
  cat("\n===== dataset", dset, "\nindependent raw wilcox:", signif(raw, 4), "\nindependent holm:", signif(p.adjust(raw, "holm"), 4), "\nindependent bonf:", signif(p.adjust(raw, "bonferroni"), 4), "\nindependent BH:", signif(p.adjust(raw, "BH"), 4), "\n")
  cat("kruskal p:", kruskal.test(value ~ group, df)$p.value, "\n")

  # --- SKILL.md block: ggboxplot + stat_compare_means(comparisons, wilcox, holm, p.signif)
  for (lab in c("p.signif", "p.format")) {
    p1 <- ggboxplot(df, x = 'group', y = 'value', color = 'group', add = 'jitter', palette = 'npg') +
      stat_compare_means(method = 'wilcox.test', comparisons = prs, label = lab, p.adjust.method = 'holm',
                         method.args = list(alternative = 'two.sided'))
    ggsave(file.path(F, paste0("s1_", dset, "_", lab, ".png")), p1, width = 6, height = 5, dpi = 100)
    b <- ggplot_build(p1)
    for (i in seq_along(b$data)) { ld <- b$data[[i]]; if ("annotations" %in% names(ld)) { cat("label=", lab, " layer", i, "annotations:", as.character(ld$annotations), " x:", ld$x, " xend:", ld$xend, " y:", signif(ld$y,4), "\n") } }
  }
}

# default method of stat_compare_means (claim: t-test)
df <- read.csv(file.path(D, "data", "three_group.csv")); two <- df[df$group %in% c("Control","Treatment"),]
p0 <- ggboxplot(two, x="group", y="value") + stat_compare_means()
b0 <- ggplot_build(p0); print(b0$data[[length(b0$data)]][, c("label","x","y")])
cat("truth wilcox Control-Treatment:", wilcox.test(value~group, two)$p.value, " welch:", t.test(value~group, two)$p.value, "\n")
print(compare_means(value ~ group, two))
# default with >2 groups
p00 <- ggboxplot(df, x="group", y="value") + stat_compare_means()
print(ggplot_build(p00)$data[[2]][, c("label")]); cat("KW truth", kruskal.test(value~group, df)$p.value, "anova", summary(aov(value~group, df))[[1]][["Pr(>F)"]][1], "\n")
