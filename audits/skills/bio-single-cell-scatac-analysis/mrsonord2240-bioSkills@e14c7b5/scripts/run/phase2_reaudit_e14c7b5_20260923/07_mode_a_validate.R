args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 1)
text <- paste(readLines(args[[1]], warn = FALSE), collapse = "\\n")
required <- c("Input 2", "ArchR", "SnapATAC2", "Input 6", "Input 7",
              "unsupported", "motif", "occupancy", "pseudobulk")
stopifnot(all(vapply(required, function(x) grepl(x, text, fixed = TRUE), logical(1))))
cat("mode_a_inputs_clean_exit inputs=2,6,7 direct_response_recorded=TRUE\\n")
