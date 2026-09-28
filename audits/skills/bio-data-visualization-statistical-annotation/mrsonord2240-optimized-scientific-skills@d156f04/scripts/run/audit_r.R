# Execute all seven pre-fix regression inputs plus the new nested-membership guard.

script_arg <- grep("^--file=", commandArgs(trailingOnly = FALSE), value = TRUE)
run_dir <- dirname(normalizePath(sub("^--file=", "", script_arg)))
root <- dirname(run_dir)
data_dir <- file.path(root, "data")
output_dir <- file.path(run_dir, "output")
skill_dir <- file.path(run_dir, "skill-copy")
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

source(file.path(skill_dir, "scripts", "annotate_pairwise.R"))
source(file.path(skill_dir, "scripts", "annotate_paired.R"))
source(file.path(skill_dir, "scripts", "annotate_nested.R"))

suppressPackageStartupMessages({
  library(ggplot2)
  library(ggpubr)
  library(rstatix)
})

lines <- character()
record <- function(...) {
  line <- paste(...)
  lines <<- c(lines, line)
  cat(line, "\n")
}
fmt <- function(x) paste(format(x, digits = 10), collapse = ",")

# Input 1: canonical three-group skewed comparison.
canonical <- annotate_pairwise(
  file.path(data_dir, "three_group.csv"),
  file.path(output_dir, "r_three_group_holm.png"), "wilcox", "holm"
)
stopifnot(isTRUE(all.equal(canonical$tests$p.adj,
                          p.adjust(canonical$tests$p, method = "holm"), tolerance = 1e-10)))
record("input1_raw", fmt(canonical$tests$p))
record("input1_holm", fmt(canonical$tests$p.adj))
record("input1_labels", paste(canonical$tests$p.adj.signif, collapse = ","))

# Input 2: pairing is stable under row shuffle because IDs are checked and sorted.
paired <- annotate_paired(
  file.path(data_dir, "paired.csv"), file.path(output_dir, "r_paired.png"), "holm"
)
set.seed(20260927)
paired_df <- read.csv(file.path(data_dir, "paired.csv"))
shuffled_path <- file.path(output_dir, "paired_shuffled_r.csv")
write.csv(paired_df[sample(seq_len(nrow(paired_df))), ], shuffled_path, row.names = FALSE)
paired_shuffled <- annotate_paired(
  shuffled_path, file.path(output_dir, "r_paired_shuffled.png"), "holm"
)
stopifnot(isTRUE(all.equal(paired$tests$p.adj, paired_shuffled$tests$p.adj, tolerance = 1e-15)))
record("input2_p", fmt(paired$tests$p))
record("input2_shuffled_p", fmt(paired_shuffled$tests$p))

# Input 3: the two borderline raw results must become null after Holm.
border <- annotate_pairwise(
  file.path(data_dir, "border.csv"), file.path(output_dir, "r_border_holm.png"), "wilcox", "holm"
)
stopifnot(isTRUE(all.equal(border$tests$p.adj,
                          p.adjust(border$tests$p, method = "holm"), tolerance = 1e-10)))
stopifnot(identical(as.character(border$tests$p.adj.signif), c("ns", "***", "ns")))
record("input3_raw", fmt(border$tests$p))
record("input3_holm", fmt(border$tests$p.adj))
record("input3_labels", paste(border$tests$p.adj.signif, collapse = ","))

# Input 4: full six-comparison Wilcoxon family plus Dunn and Tukey routes.
four_holm <- annotate_pairwise(
  file.path(data_dir, "four_group.csv"), file.path(output_dir, "r_four_holm.png"), "wilcox", "holm"
)
four_bonferroni <- annotate_pairwise(
  file.path(data_dir, "four_group.csv"), file.path(output_dir, "r_four_bonferroni.png"),
  "wilcox", "bonferroni"
)
four_bh <- annotate_pairwise(
  file.path(data_dir, "four_group.csv"), file.path(output_dir, "r_four_bh.png"), "wilcox", "BH"
)
four_dunn <- annotate_pairwise(
  file.path(data_dir, "four_group.csv"), file.path(output_dir, "r_four_dunn.png"), "dunn", "holm"
)
four_tukey <- annotate_pairwise(
  file.path(data_dir, "four_group.csv"), file.path(output_dir, "r_four_tukey.png"), "tukey", "tukey"
)
stopifnot(nrow(four_holm$tests) == 6L, nrow(four_bonferroni$tests) == 6L,
          nrow(four_bh$tests) == 6L,
          nrow(four_dunn$tests) == 6L, nrow(four_tukey$tests) == 6L)
stopifnot(isTRUE(all.equal(four_holm$tests$p.adj,
                          p.adjust(four_holm$tests$p, method = "holm"), tolerance = 1e-10)))
stopifnot(isTRUE(all.equal(four_bh$tests$p.adj,
                          p.adjust(four_bh$tests$p, method = "BH"), tolerance = 1e-10)))
stopifnot(isTRUE(all.equal(four_bonferroni$tests$p.adj,
                          p.adjust(four_bonferroni$tests$p, method = "bonferroni"),
                          tolerance = 1e-10)))
four_df <- read.csv(file.path(data_dir, "four_group.csv"))
independent_tukey <- as.data.frame(TukeyHSD(aov(value ~ factor(group), data = four_df))[[1]])
stopifnot(isTRUE(all.equal(sort(four_tukey$tests$p.adj),
                          sort(independent_tukey$`p adj`), tolerance = 1e-8)))
record("input4_holm", fmt(four_holm$tests$p.adj))
record("input4_bonferroni", fmt(four_bonferroni$tests$p.adj))
record("input4_bh", fmt(four_bh$tests$p.adj))
record("input4_dunn", fmt(four_dunn$tests$p.adj))
record("input4_tukey", fmt(four_tukey$tests$p.adj))

# Input 5: model-based nested contrast, not a cell-level test.
nested <- annotate_nested(
  file.path(data_dir, "nested.csv"), file.path(output_dir, "r_nested.png"), "holm"
)
stopifnot(nrow(nested$tests) == 1L, is.finite(nested$tests$p.adj[[1]]),
          nested$tests$p.adj[[1]] > 0.05)
record("input5_lmm_p", fmt(nested$tests$p.adj))

# Input 6: exact p, significance, and magnitude for a very large sample.
big <- read.csv(file.path(data_dir, "bigN.csv"))
big$group <- factor(big$group, levels = unique(big$group))
groups <- levels(big$group)
x <- big$value[big$group == groups[[1]]]
y <- big$value[big$group == groups[[2]]]
big_test <- wilcox.test(x, y, exact = FALSE)
pooled_sd <- sqrt(((length(x) - 1) * var(x) + (length(y) - 1) * var(y)) /
                  (length(x) + length(y) - 2))
cohen_d <- (mean(y) - mean(x)) / pooled_sd
big_result <- data.frame(
  group1 = groups[[1]], group2 = groups[[2]], p.adj = big_test$p.value,
  p.adj.signif = case_when(big_test$p.value <= 1e-4 ~ "****",
                           big_test$p.value <= 0.001 ~ "***",
                           big_test$p.value <= 0.01 ~ "**",
                           big_test$p.value <= 0.05 ~ "*",
                           TRUE ~ "ns")
) |>
  add_y_position(formula = value ~ group, data = big)
big_result$display_label <- paste0("p = ", format(big_test$p.value, digits = 4),
                                   " (", big_result$p.adj.signif, ")")
big_plot <- ggboxplot(big, x = "group", y = "value", color = "group",
                      add = "jitter", outlier.shape = NA) +
  stat_pvalue_manual(big_result,
                     label = "display_label",
                     tip.length = 0.01) +
  labs(caption = sprintf("Wilcoxon rank-sum; Cohen's d = %.3f.", cohen_d)) +
  theme_classic() + theme(legend.position = "none")
ggsave(file.path(output_dir, "r_bigN_exact_effect.png"), big_plot,
       width = 6.5, height = 5.5, dpi = 160)
write.csv(data.frame(test = "Wilcoxon rank-sum", p = big_test$p.value,
                     p_adj = big_test$p.value, cohen_d = cohen_d),
          file.path(output_dir, "r_bigN_exact_effect.results.csv"), row.names = FALSE)
stopifnot(big_test$p.value < 1e-5, abs(cohen_d) < 0.15)
record("input6_p", fmt(big_test$p.value))
record("input6_cohen_d", fmt(cohen_d))

# Input 7: the installed ggpubr default is Wilcoxon/Kruskal-Wallis, not t/ANOVA.
two_group <- droplevels(subset(read.csv(file.path(data_dir, "three_group.csv")),
                               group %in% c("Control", "Treatment")))
default_two <- ggplot(two_group, aes(group, value)) + geom_boxplot() + stat_compare_means()
default_three_df <- read.csv(file.path(data_dir, "three_group.csv"))
default_three <- ggplot(default_three_df, aes(group, value)) + geom_boxplot() + stat_compare_means()
two_labels <- unlist(lapply(ggplot_build(default_two)$data, function(layer) {
  if ("label" %in% names(layer)) as.character(layer$label) else character()
}))
three_labels <- unlist(lapply(ggplot_build(default_three)$data, function(layer) {
  if ("label" %in% names(layer)) as.character(layer$label) else character()
}))
stopifnot(any(grepl("Wilcoxon", two_labels)), any(grepl("Kruskal-Wallis", three_labels)))
ggsave(file.path(output_dir, "r_default_two.png"), default_two, width = 5.5, height = 5, dpi = 160)
ggsave(file.path(output_dir, "r_default_three.png"), default_three, width = 5.5, height = 5, dpi = 160)
record("input7_two_default", paste(two_labels, collapse = " | "))
record("input7_three_default", paste(three_labels, collapse = " | "))

# New input 9: reject cross-group reuse of one biological subject ID.
invalid_error <- tryCatch({
  annotate_nested(file.path(data_dir, "nested_cross_group_subject.csv"),
                  file.path(output_dir, "must_not_exist_nested.png"), "holm")
  NA_character_
}, error = function(error) conditionMessage(error))
stopifnot(!is.na(invalid_error), grepl("exactly one group", invalid_error, fixed = TRUE),
          !file.exists(file.path(output_dir, "must_not_exist_nested.png")))
record("input9_error", invalid_error)

writeLines(lines, file.path(output_dir, "r_metrics.txt"), useBytes = TRUE)
cat("R re-audit assertions passed\n")
