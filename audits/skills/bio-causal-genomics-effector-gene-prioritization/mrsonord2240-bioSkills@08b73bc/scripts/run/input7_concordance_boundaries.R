suppressPackageStartupMessages(library(dplyr))

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 1) stop("usage: input7_concordance_boundaries.R <out_prefix>")
prefix <- args[1]
out <- read.table(paste0(prefix, ".scored.tsv"), header = TRUE, sep = "\t", stringsAsFactors = FALSE)
row_exact <- out[out$gene == "EXACT", ]
row_strict <- out[out$gene == "STRICT", ]
row_na <- out[out$gene == "MISSING", ]
stopifnot(nrow(row_exact) == 1L, nrow(row_strict) == 1L, nrow(row_na) == 1L)
stopifnot(row_exact$concordance == 6L, row_exact$confidence_tier == "near_certain")
stopifnot(row_strict$concordance == 5L, row_strict$confidence_tier == "near_certain")
stopifnot(row_na$concordance == 0L, row_na$n_streams_available == 0L, row_na$confidence_tier == "associational_only")
cat("ASSERTIONS PASS: inclusive threshold row=6/6; strict PIP=0.5 row=5/near_certain; all-NA row retained as 0/0 associational_only.\n")
