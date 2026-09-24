args <- commandArgs(trailingOnly = TRUE)
for (path in args) {
  expr <- parse(file = path)
  stopifnot(length(expr) > 0L)
  cat(sprintf("r_parse_clean_exit file=%s expressions=%d\n", path, length(expr)))
}
