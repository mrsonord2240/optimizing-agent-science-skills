library(GenomicSEM)
b <- deparse(body(commonfactor))
idx <- grep("sem\\(|cfa\\(|tryCatch", b)
for (i in idx) cat(i, ": ", b[i], "\n")
cat("\n--- context around each sem() call (10 lines before/after) ---\n")
for (i in grep("<- *sem\\(", b)) {
  cat("\n---- block near line", i, "----\n")
  cat(paste(b[max(1,i-15):min(length(b), i+25)], collapse="\n"), "\n")
}
