suppressPackageStartupMessages({
  library(ggseqlogo)
  library(ggplot2)
})

glyph_tops <- function(plot) {
  d <- plot$layers[[1]]$data
  d <- d[!is.na(d$position) & !is.na(d$letter), ]
  by_pos <- split(d, d$position)
  vapply(by_pos, function(x) max(x$y), numeric(1))
}

seqs <- rep("AA", 5)
seq_plot <- ggseqlogo(seqs, method = "bits")
expected_sequence <- 2 - 3 / (2 * log(2) * 5)
stopifnot(abs(unname(glyph_tops(seq_plot))[1] - expected_sequence) < 1e-6)

counts <- matrix(c(5, 0, 0, 0, 5, 0, 0, 0), nrow = 4,
                 dimnames = list(c("A", "C", "G", "T"), NULL))
matrix_plot <- ggseqlogo(counts, method = "bits")
stopifnot(abs(unname(glyph_tops(matrix_plot))[1] - 2) < 1e-6)

transposed <- t(matrix(c(0.7, 0.1, 0.1, 0.1,
                         0.1, 0.7, 0.1, 0.1),
                       nrow = 4,
                       dimnames = list(c("A", "C", "G", "T"), NULL)))
orientation_error <- tryCatch({
  ggseqlogo(transposed, method = "bits")
  FALSE
}, error = function(e) grepl("letters for row names", conditionMessage(e), fixed = TRUE))
stopifnot(orientation_error)

cat(sprintf("sequence_n5=%.9f\n", unname(glyph_tops(seq_plot))[1]))
cat(sprintf("matrix_n5=%.9f\n", unname(glyph_tops(matrix_plot))[1]))
cat("orientation_error=TRUE\n")
