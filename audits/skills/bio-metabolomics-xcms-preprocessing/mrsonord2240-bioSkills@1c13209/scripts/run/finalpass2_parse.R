# Parse check for every executable Phase 2 audit input.
paths <- list.files("F:/OpenScience/audits/bio-metabolomics-xcms-preprocessing/run",
                    pattern = "^finalpass2_input.*\\.R$", full.names = TRUE)
paths <- c(paths, "F:/OpenScience/wt/metabolomics-xcms-preprocessing/metabolomics/xcms-preprocessing/examples/xcms_workflow.R")
for (path in paths) {
  parse(path)
  cat("PARSE PASS:", basename(path), "\n")
}
stopifnot(length(paths) == 8)
