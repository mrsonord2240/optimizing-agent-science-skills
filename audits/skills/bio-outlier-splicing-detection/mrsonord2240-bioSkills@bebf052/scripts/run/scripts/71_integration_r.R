# Run SKILL.md integration R block (blocks/07_r.R) verbatim in a dir holding spliceai_raw.tsv + fraser_results.tsv; print + assert
a <- commandArgs(TRUE); setwd(a[1]); expect <- a[3]
r <- try(source(a[2], echo = FALSE), silent = TRUE)
if (inherits(r, "try-error")) { cat("BLOCK ERROR:", conditionMessage(attr(r, "condition")), "\n"); quit(status = 0) }
cat("variants parsed:", nrow(raw), "; delta_max values:", paste(round(raw$delta_max, 2), collapse = " "), "\n")
print(as.data.frame(confirmed)[, intersect(c("chrom", "pos", "delta_max", "start", "end", "sampleID", "padjust", "deltaPsi"), names(confirmed))])
cat("confirmed positions:", paste(sort(unique(confirmed$pos)), collapse = ","), "| expected:", expect, "\n")
stopifnot(identical(paste(sort(unique(confirmed$pos)), collapse = ","), expect))
cat("ASSERT OK\n")
