# Deterministic numerical and ggseqlogo API checks for relative_entropy_logo.R.
# Run from this examples directory.

source("relative_entropy_logo.R")

background <- c(A = 0.29, C = 0.21, G = 0.21, T = 0.29)
probabilities <- cbind(
    pure_c = c(A = 0, C = 1, G = 0, T = 0),
    background_matched = background
)
heights <- relative_entropy_heights(probabilities, background)

stopifnot(
    isTRUE(all.equal(sum(heights[, "pure_c"]), -log2(background[["C"]]), tolerance = 1e-12)),
    isTRUE(all.equal(sum(heights[, "background_matched"]), 0, tolerance = 1e-12)),
    isTRUE(all.equal(attr(heights, "relative_entropy_bits"), colSums(heights), tolerance = 1e-12))
)

fixture <- read_aligned_fasta("aligned_motif.fa")
fixture_heights <- relative_entropy_heights(
    sequence_probability_matrix(fixture, names(background)), background
)
stopifnot(
    nrow(fixture_heights) == 4L,
    ncol(fixture_heights) == nchar(fixture[[1]]),
    all(is.finite(fixture_heights)),
    all(colSums(fixture_heights) >= 0)
)

library(ggseqlogo)
custom_plot <- ggseqlogo(heights[, "pure_c", drop = FALSE], method = "custom")
plotted_layer <- ggplot2::ggplot_build(custom_plot)$data[[1]]
stopifnot(
    inherits(custom_plot, "ggplot"),
    isTRUE(all.equal(max(plotted_layer$y), -log2(background[["C"]]), tolerance = 1e-12))
)
message("relative-entropy logo checks passed")
