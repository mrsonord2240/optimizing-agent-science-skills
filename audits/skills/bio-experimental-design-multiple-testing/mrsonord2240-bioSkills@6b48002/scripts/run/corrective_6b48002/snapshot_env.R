# Capture the audit environment's installed package versions (read-only).
# Usage: r.sh snapshot_env.R <output-file>
args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 1L)
ip <- installed.packages()
keep <- c("IHW", "qvalue", "stats")
rows <- data.frame(package = keep,
                   version = vapply(keep, function(x) as.character(packageVersion(x)), character(1)),
                   stringsAsFactors = FALSE)
write.csv(rows, args[[1]], row.names = FALSE)
