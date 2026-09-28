# Fixer evidence: execute the shipped Dunn and Tukey modes on the four-group audit fixture.
source("F:/OpenScience/wt/backlog-statistical-annotation/skills/bio-data-visualization-statistical-annotation/scripts/annotate_pairwise.R")
data <- "F:/OpenScience/audits/bio-data-visualization-statistical-annotation/data/four_group.csv"
out <- "F:/OpenScience/audits/bio-data-visualization-statistical-annotation/run/fixer-output"
dunn <- annotate_pairwise(data, file.path(out, "r-four-dunn-runner.png"), "dunn", "holm")
stopifnot(nrow(dunn$tests) == 6L, all(is.finite(dunn$tests$p.adj)))
cat("DUNN PASS", paste(signif(dunn$tests$p.adj, 6), collapse = " "), "\n")
tukey <- annotate_pairwise(data, file.path(out, "r-four-tukey-runner.png"), "tukey", "tukey")
stopifnot(nrow(tukey$tests) == 6L, all(is.finite(tukey$tests$p.adj)))
cat("TUKEY PASS", paste(signif(tukey$tests$p.adj, 6), collapse = " "), "\n")
