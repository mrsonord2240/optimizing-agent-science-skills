args <- commandArgs(trailingOnly = TRUE)
obj <- readRDS(args[[1]])
cat(paste(colnames(obj[[]]), collapse = "\n"), "\n")
for (nm in colnames(obj[[]])) {
  x <- obj[[nm]][, 1]
  if (is.character(x) || is.factor(x) || is.integer(x)) {
    vals <- unique(as.character(x))
    if (length(vals) <= 20L) cat(sprintf("%s: %s\n", nm, paste(vals, collapse = ",")))
  }
}
