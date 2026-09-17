# Input 8 (NEW) -- "Run the shipped Class-Based Internal-Standard
# Quantification example exactly as SKILL.md documents it, on real data."
#
# This is a NEW input (not in the pre-fix audit): it runs SKILL.md's own
# "Class-Based Internal-Standard Quantification" code block close to
# verbatim, against lipidr's own bundled RAW Skyline export (A1/F1/F2 +
# clin.csv), which the fix swapped in because lipidr's shipped
# `data_normalized` is already PQN-normalized and normalize_istd() refuses to
# run on already-normalized data ("Area is already normalized").
#
# Two things checked: (1) the shipped example now runs end-to-end on real
# data instead of crashing, and (2) the istd-coverage guard does NOT
# false-positive-refuse real data where every class IS actually covered
# (dispatch's explicit ask: "check that it does not now refuse data it
# should accept").
suppressMessages(library(lipidr))

datadir <- system.file("extdata", package = "lipidr")
d_raw <- add_sample_annotation(
  read_skyline(list.files(datadir, "A1_data.csv|F1_data.csv|F2_data.csv", full.names = TRUE)),
  file.path(datadir, "clin.csv")
)
cat("Loaded lipidr's own raw shipped Skyline export:", nrow(d_raw), "lipids x", ncol(d_raw), "samples\n")
cat("Classes detected:", length(unique(rowData(d_raw)$Class)), "->",
    paste(unique(rowData(d_raw)$Class), collapse = ", "), "\n\n")

istd_coverage <- table(rowData(d_raw)$Class, rowData(d_raw)$istd)
uncovered <- rownames(istd_coverage)[
  !("TRUE" %in% colnames(istd_coverage)) | istd_coverage[, "TRUE"] == 0
]
cat("=== Guard check on REAL, fully-covered data ===\n")
cat("Uncovered classes found:", if (length(uncovered) == 0) "(none)" else paste(uncovered, collapse = ", "), "\n")
stopifnot(length(uncovered) == 0)  # must NOT false-positive here -- every class has a standard
cat("PASS: guard does not false-positive-refuse real, fully-covered data\n\n")

d_istd <- normalize_istd(d_raw, measure = "Area", exclude = "blank", log = TRUE)
cat("=== normalize_istd() on real data ===\n")
cat("Completed:", nrow(d_istd), "lipids x", ncol(d_istd), "samples, no error\n\n")

plt <- plot_lipidclass(d_istd, "sd")
out_path <- "../data/input8_lipidclass_sd.png"
ggplot2::ggsave(out_path, plt, width = 8, height = 5)
sz <- file.info(out_path)$size
cat("Saved", out_path, "--", sz, "bytes\n")
stopifnot(!is.na(sz) && sz > 1000)  # must be a real, non-empty rendered plot
cat("PASS: shipped example runs end-to-end and renders a real, non-empty plot\n")
