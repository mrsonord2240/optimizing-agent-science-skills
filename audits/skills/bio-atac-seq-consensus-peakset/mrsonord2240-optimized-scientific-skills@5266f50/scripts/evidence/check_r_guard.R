args <- commandArgs(trailingOnly = TRUE)
methods_path <- args[[1]]
lines <- readLines(methods_path, warn = FALSE)
r_fence <- which(lines == "```r")
stopifnot(length(r_fence) == 1L)
r_end <- which(seq_along(lines) > r_fence & lines == "```")[[1]]
r_block <- lines[(r_fence + 1L):(r_end - 1L)]
parse(text = r_block, keep.source = FALSE)
guard_start <- which(r_block == "peak_offset <- peaks$peak")
stopifnot(length(guard_start) == 1L)
guard_source <- r_block[guard_start:(guard_start + 4L)]
width <- function(peaks) peaks$widths
length.peak_mock <- function(x) x$count
guard <- eval(parse(text = paste(c("function(peaks) {", guard_source, "peak_offset", "}"), collapse = "\n")))
mock <- function(peak, widths, count = length(widths)) {
    structure(list(peak = peak, widths = widths, count = count), class = "peak_mock")
}
expect_reject <- function(x, label) {
    message <- tryCatch({ guard(x); "" }, error = function(e) conditionMessage(e))
    stopifnot(grepl("summit offsets must be present and within each interval", message, fixed = TRUE))
    cat("REJECT", label, "\n")
}
valid <- guard(mock(c(0L, 99L), c(100L, 100L)))
stopifnot(identical(valid, c(0L, 99L)))
cat("ACCEPT lower and upper valid offsets: 0, 99\n")
expect_reject(mock(-1L, 100L), "-1 sentinel")
expect_reject(mock(-2L, 100L), "other negative offset")
expect_reject(mock(NA_integer_, 100L), "missing offset")
expect_reject(mock(100L, 100L), "offset equal to interval width")
expect_reject(mock(1L, c(100L, 100L), count = 2L), "offset/feature count mismatch")
expect_reject(mock(NULL, 100L), "absent offset field")
cat("R guard checks passed; the exact guard expression runs before the example's start-coordinate assignment.\n")
