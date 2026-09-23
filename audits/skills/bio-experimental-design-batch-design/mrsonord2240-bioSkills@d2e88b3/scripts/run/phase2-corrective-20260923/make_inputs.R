# Synthetic audit inputs for the documented command-line workflows.
set.seed(20260923)
samples24 <- data.frame(
  id = sprintf("S%02d", 1:24),
  condition = rep(c("ctrl", "case"), each = 12),
  sex = rep(rep(c("F", "M"), each = 2), 6),
  stringsAsFactors = FALSE
)
write.csv(samples24, "samples24.csv", row.names = FALSE)

samples60 <- data.frame(
  id = sprintf("P%02d", 1:60),
  condition = rep(c("ctrl", "case"), each = 30),
  site = rep(c("A", "B", "C"), length.out = 60),
  stringsAsFactors = FALSE
)
write.csv(samples60, "samples60.csv", row.names = FALSE)

bad_samples <- samples24[, c("id", "condition")]
write.csv(bad_samples, "missing_sex.csv", row.names = FALSE)
cat("Wrote samples24.csv (", nrow(samples24), " rows), samples60.csv (", nrow(samples60), " rows), and missing_sex.csv.\n", sep = "")
