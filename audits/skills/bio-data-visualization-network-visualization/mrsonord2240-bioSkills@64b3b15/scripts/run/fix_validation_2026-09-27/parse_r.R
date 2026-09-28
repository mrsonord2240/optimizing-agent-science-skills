# Parse every changed R script without evaluating it.
# Usage: Rscript validation/parse_r.R script1.R [script2.R ...]
args <- commandArgs(trailingOnly = TRUE)
if (length(args) == 0) stop("Pass at least one R script")
for (path in args) {
  expressions <- parse(file = path, encoding = "UTF-8")
  message("PARSE ", path, ": ", length(expressions), " expressions")
}
