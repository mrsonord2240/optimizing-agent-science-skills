# Input 1 (Canonical) -- real hand-off test: does the workflow's own Stage1->Stage2
# code snippet (fm <- t(feat)) actually produce the orientation pmp needs?
suppressMessages(library(pmp))

feat_tab <- read.csv("F:/OpenScience/audits/bio-metabolomics-xcms-preprocessing/run/feature_table_input1.csv",
                      row.names = 1, check.names = FALSE)
# feat_tab has columns mz, rt, then 12 real sample columns (real xcms featureValues() output
# from the xcms-preprocessing audit, 574 real faahKO features x 12 real samples)
feat <- as.matrix(feat_tab[, setdiff(colnames(feat_tab), c("mz", "rt"))])
cat("Real xcms featureValues() output (as documented, features x samples):", dim(feat)[1], "x", dim(feat)[2], "\n")
cat("This already matches the workflow's own stated pmp convention: features in ROWS, samples in COLUMNS.\n\n")

# Workflow SKILL.md Stage 2 code, verbatim:
#   fm <- t(feat)   # comment says: "features in ROWS, samples in COLUMNS (pmp convention)"
fm <- t(feat)
cat("After the workflow's documented `fm <- t(feat)`:", dim(fm)[1], "x", dim(fm)[2], "\n")
cat("-> rows are now SAMPLES, columns are now FEATURES -- the OPPOSITE of the comment's own claim.\n\n")

sample_group <- c(rep("KO", 6), rep("WT", 6))
names(sample_group) <- colnames(feat)

cat("=== Attempt A: run filter_peaks_by_fraction on `fm` exactly as the workflow's code hands it off ===\n")
res_wrong <- tryCatch({
  filter_peaks_by_fraction(df = fm, min_frac = 0.5, classes = sample_group, qc_label = "KO")
}, error = function(e) e, warning = function(w) w)
if (inherits(res_wrong, "error") || inherits(res_wrong, "warning")) {
  cat("Condition raised:", conditionMessage(res_wrong), "\n")
} else {
  cat("No error/warning. Returned dim:", paste(dim(res_wrong), collapse=" x "), "\n")
  cat("Interpreted as: filtering", ifelse(nrow(res_wrong)==nrow(fm), "rows (samples!)", "something"),
      "instead of features -- silently wrong, not caught by pmp.\n")
}

cat("\n=== Attempt B: run filter_peaks_by_fraction on the UN-transposed `feat` (the orientation actually needed) ===\n")
res_right <- tryCatch({
  filter_peaks_by_fraction(df = feat, min_frac = 0.5, classes = sample_group, qc_label = "KO")
}, error = function(e) e, warning = function(w) w)
if (inherits(res_right, "error") || inherits(res_right, "warning")) {
  cat("Condition raised:", conditionMessage(res_right), "\n")
} else {
  cat("No error/warning. Returned dim:", paste(dim(res_right), collapse=" x "), "of", paste(dim(feat), collapse=" x "), "\n")
}
