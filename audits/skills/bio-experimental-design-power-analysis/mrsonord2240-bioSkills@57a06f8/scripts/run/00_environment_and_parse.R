skill_dir <- "F:/OpenScience/wt/experimental-design-power-analysis/experimental-design/power-analysis"
files <- c(file.path(skill_dir, "SKILL.md"), file.path(skill_dir, "usage-guide.md"), file.path(skill_dir, "examples/rnaseq_power.R"), file.path(skill_dir, "examples/scrna_pseudobulk_power.R"))
stopifnot(all(file.exists(files)))
for (f in files[3:4]) parse(f)
for (pkg in c("RNASeqPower", "PROPER", "edgeR", "pwr")) {
  suppressPackageStartupMessages(library(pkg, character.only = TRUE))
  cat(sprintf("%s=%s\n", pkg, as.character(packageVersion(pkg))))
}
cat("PARSE_AND_ENVIRONMENT=PASS\n")
