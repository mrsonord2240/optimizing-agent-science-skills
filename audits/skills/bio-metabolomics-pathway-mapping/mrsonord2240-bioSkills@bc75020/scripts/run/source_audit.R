suppressMessages(library(MetaboAnalystR))
options(width=200)

show_src <- function(fname, ns="MetaboAnalystR") {
  cat("\n=====", fname, "=====\n")
  f <- tryCatch(getFromNamespace(fname, ns), error=function(e) NULL)
  if (is.null(f)) { cat("NOT FOUND\n"); return(invisible(NULL)) }
  src <- deparse(f)
  hits <- grep("POST|GET|http|url|curl|download|api|Server|readLines|RCurl|httr|remote", src, ignore.case=TRUE)
  if (length(hits)==0) { cat("(no obvious network tokens found; printing first 15 lines)\n"); print(head(src,15)); return(invisible(NULL)) }
  for (i in hits) {
    lo <- max(1, i-2); hi <- min(length(src), i+2)
    cat(sprintf("--- lines %d-%d ---\n", lo, hi))
    cat(paste(src[lo:hi], collapse="\n"), "\n")
  }
}

for (fn in c("CrossReferencing", "Setup.MapData", "SetKEGG.PathLib", "Setup.KEGGReferenceMetabolome",
             "CalculateQeaScore", "my.qea.kegg", "PerformPSEA", "SetPeakEnrichMethod",
             "SanityCheckMummichogData", "Read.PeakListData", ".do.api.call", "my.ora.kegg",
             "InitDataObjects", "SetOrganism")) {
  show_src(fn)
}
