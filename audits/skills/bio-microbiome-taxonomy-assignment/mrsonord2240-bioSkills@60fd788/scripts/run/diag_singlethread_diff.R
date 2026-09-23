# Diagnose WHY seeded single-threaded assignTaxonomy() runs (run4 vs run5, both set.seed(100),
# both multithread=FALSE) are identical()==FALSE. Is this a real data difference (the "seeded fix"
# claim would be wrong for single-threaded use) or a spurious attribute/environment artifact that
# identical() catches but the actual classification data does not differ?
.libPaths(c("F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/R-lib", .libPaths()))

dir <- "F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/myreaudit"
single_reruns <- readRDS(file.path(dir, "assigntax_single_reruns.rds"))
s4 <- single_reruns$s4
s5 <- single_reruns$s5

cat("class(s4):", class(s4), "\n")
cat("class(s5):", class(s5), "\n")
cat("dim(s4):", dim(s4), "  dim(s5):", dim(s5), "\n")
cat("identical(dimnames(s4), dimnames(s5)):", identical(dimnames(s4), dimnames(s5)), "\n")
cat("identical(attributes(s4), attributes(s5)):", identical(attributes(s4), attributes(s5)), "\n")

cat("\nnames(attributes(s4)):", paste(names(attributes(s4)), collapse=", "), "\n")
cat("names(attributes(s5)):", paste(names(attributes(s5)), collapse=", "), "\n")

# Strip all attributes except dim/dimnames and compare raw data
s4_raw <- s4; attributes(s4_raw)[!(names(attributes(s4_raw)) %in% c("dim","dimnames"))] <- NULL
s5_raw <- s5; attributes(s5_raw)[!(names(attributes(s5_raw)) %in% c("dim","dimnames"))] <- NULL
cat("\nidentical(s4_raw, s5_raw) [attributes other than dim/dimnames stripped]:", identical(s4_raw, s5_raw), "\n")

cat("\nall.equal(s4, s5):\n")
print(all.equal(s4, s5))

cat("\nPer-rank cell-value differences (raw data, ignoring attrs), s4 vs s5:\n")
for (rank in colnames(s4)) {
  d <- sum(s4[, rank] != s5[, rank] | (is.na(s4[, rank]) != is.na(s5[, rank])), na.rm = TRUE) +
       sum(is.na(s4[, rank]) != is.na(s5[, rank]))
  cat(sprintf("  %-8s differing: %d / %d\n", rank, d, nrow(s4)))
}

# Also check: does DIMNAMES order/content differ (row order of ASVs)?
cat("\nidentical(rownames(s4), rownames(s5)):", identical(rownames(s4), rownames(s5)), "\n")
cat("identical(colnames(s4), colnames(s5)):", identical(colnames(s4), colnames(s5)), "\n")

# Full raw value equality check (values only, via table comparison), regardless of row/col order
cat("\nsum(s4_raw == s5_raw, na.rm=TRUE) vs total non-NA cells:\n")
eq <- (s4_raw == s5_raw)
cat("TRUE cells:", sum(eq, na.rm=TRUE), " / non-NA comparisons:", sum(!is.na(eq)), " / total cells:", length(eq), "\n")
cat("NA-mismatch cells (one NA, other not):", sum(is.na(s4_raw) != is.na(s5_raw)), "\n")
cat("Done.\n")
