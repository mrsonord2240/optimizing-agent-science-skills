# Fixer evidence: parse every changed R file and record installed versions.
root <- "F:/OpenScience/wt/backlog-statistical-annotation/skills/bio-data-visualization-statistical-annotation"
files <- c(
  file.path(root, "scripts", "annotate_pairwise.R"),
  file.path(root, "scripts", "annotate_paired.R"),
  file.path(root, "scripts", "annotate_nested.R"),
  file.path(root, "examples", "statanno_phd.R"),
  file.path(root, "tests", "regression.R")
)
for (file in files) {
  parse(file = file)
  cat("PARSE PASS", basename(file), "\n")
}
for (pkg in c("ggpubr", "ggsignif", "rstatix", "lme4", "emmeans", "ggplot2")) {
  cat(pkg, as.character(packageVersion(pkg)), "\n")
}
