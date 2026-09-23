# Phase 2 Input 8: syntax check the current CellChat/NicheNet references and example, then record dependency availability.
skill_dir <- "F:/OpenScience/wt/single-cell-cell-communication/single-cell/cell-communication"
paths <- c(
  file.path(skill_dir, "references", "cellchat.md"),
  file.path(skill_dir, "references", "nichenet.md"),
  file.path(skill_dir, "examples", "cellchat_analysis.R")
)
extract_r_fences <- function(path) {
  lines <- readLines(path, warn = FALSE)
  starts <- which(grepl("^```r$", lines))
  for (start in starts) {
    stop_at <- which(seq_along(lines) > start & grepl("^```$", lines))[1]
    code <- lines[(start + 1):(stop_at - 1)]
    parse(text = code)
  }
  TRUE
}
for (path in paths[1:2]) {
  stopifnot(extract_r_fences(path))
  cat("PARSE_OK", basename(path), "\n")
}
parse(file = paths[3])
cat("PARSE_OK", basename(paths[3]), "\n")
cat("CELLCHAT_AVAILABLE", requireNamespace("CellChat", quietly = TRUE), "\n")
cat("NICHENETR_AVAILABLE", requireNamespace("nichenetr", quietly = TRUE), "\n")
