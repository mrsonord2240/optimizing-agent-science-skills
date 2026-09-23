args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 2)
for (path in args) {
  parsed <- parse(file = path)
  stopifnot(length(parsed) > 0L)
  cat(sprintf("parse_clean_exit file=%s expressions=%d\\n", path, length(parsed)))
}
