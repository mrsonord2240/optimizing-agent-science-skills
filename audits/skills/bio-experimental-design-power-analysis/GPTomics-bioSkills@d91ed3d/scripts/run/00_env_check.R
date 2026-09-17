cat("R version:", R.version.string, "\n")
for (p in c("RNASeqPower","PROPER","DESeq2","edgeR","pwr","IHW","qvalue")) {
  ok <- requireNamespace(p, quietly = TRUE)
  ver <- if (ok) as.character(packageVersion(p)) else "MISSING"
  cat(sprintf("%-15s %s\n", p, ver))
}
cat("\n--- PROPER::comparePower delta doc check ---\n")
if (requireNamespace("PROPER", quietly = TRUE)) {
  library(PROPER)
  # print the help text body for comparePower to check delta's documented units
  db <- tools::Rd_db("PROPER")
  nm <- grep("comparePower", names(db), value = TRUE)
  print(nm)
  if (length(nm) > 0) {
    rd <- db[[nm[1]]]
    txt <- capture.output(tools::Rd2txt(rd))
    cat(paste(txt, collapse = "\n"))
  }
}
