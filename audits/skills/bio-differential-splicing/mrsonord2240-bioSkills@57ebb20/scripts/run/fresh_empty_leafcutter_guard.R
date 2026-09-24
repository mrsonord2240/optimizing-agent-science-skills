# Fresh final-pass input: execute the new zero-intron guard from the example.
# Usage: Rscript fresh_empty_leafcutter_guard.R <scratch directory>
args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 1L)
dir.create(args[[1]], recursive = TRUE, showWarnings = FALSE)
counts_file <- file.path(args[[1]], "leafcutter_perind_numers.counts.gz")
con <- gzfile(counts_file, "wt")
writeLines("intron\tcontrol1\ttreatment1", con)
close(con)
if (!file.exists(counts_file)) {
    stop("guard setup failed")
}
counts_rows <- length(readLines(gzfile(counts_file), warn = FALSE)) - 1L
message <- tryCatch({
    if (counts_rows < 1L) {
        stop("Clustering produced zero introns. Use -k True for nonstandard contigs, lower -m for shallow data, and verify BAM XS tags.")
    }
    "no error"
}, error = function(e) conditionMessage(e))
stopifnot(grepl("zero introns", message, fixed = TRUE), grepl("-k True", message, fixed = TRUE))
cat("PASS: zero-intron guard gives actionable -k/-m/XS guidance\n")
