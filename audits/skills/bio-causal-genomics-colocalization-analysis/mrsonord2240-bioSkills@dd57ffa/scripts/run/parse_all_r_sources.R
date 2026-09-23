# Parse-only verification of every shipped R script and example at the audited tip.
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 1) stop("usage: parse_all_r_sources.R <skill-root>")
files <- list.files(args[[1]], pattern="\\.R$", recursive=TRUE, full.names=TRUE)
stopifnot(length(files) == 10)
for (f in files) {
  parse(f)
  cat("PARSE PASS", normalizePath(f, winslash="/"), "\n")
}
