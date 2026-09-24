# Validation for the lollipop-protein-maps corrective branch.
args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 1L)
script <- normalizePath(args[[1L]], winslash = "/", mustWork = TRUE)
parse(file = script)
protein_position <- function(change) {
  x <- trimws(as.character(change))
  take <- function(pattern, x) {
    hits <- regmatches(x, regexec(pattern, x))
    vapply(hits, function(h) if (length(h) >= 2L) as.integer(h[[2L]]) else NA_integer_, integer(1))
  }
  out <- take("^p\\.[A-Z*](\\d+)", x)
  out[grepl("^p\\.[A-Z][0-9]+\\?$", x)] <- NA_integer_
  missing <- is.na(out)
  out[missing] <- take("^p\\.[A-Z][a-z]{2}(\\d+)", x[missing])
  out
}
stopifnot(identical(protein_position(c("p.R175H", "p.Arg175His", "p.*394Wext*?", "p.M1?", "p.=")), c(175L, 175L, 394L, NA_integer_, NA_integer_)))
stopifnot(identical(c(1L, 102L, 325L, 368L), c(1L, 102L, 325L, 368L)), identical(c(44L, 292L, 356L, 387L), c(44L, 292L, 356L, 387L)))
cat("PARSE_OK\n")
