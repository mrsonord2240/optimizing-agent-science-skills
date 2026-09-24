# SKILL Common Errors row: bambu::prepareAnnotations on an empty GTF and on a GTF whose rows were cut to 6 columns -> "Input annotation file not readable..."; and the awk check named in the row.
suppressMessages(library(bambu))
d <- tempfile(); dir.create(d); setwd(d)
g <- readLines("F:/OpenScience/audits/bio-long-read-splicing/run/data/plant/ref.gtf")
writeLines(character(0), "empty.gtf")
writeLines(vapply(strsplit(g, "\t"), function(x) paste(x[1:6], collapse = "\t"), ""), "cut6.gtf")
for (f in c("empty.gtf", "cut6.gtf")) {
  r <- tryCatch({ prepareAnnotations(f); "NO ERROR" }, error = function(e) conditionMessage(e))
  cat(f, "->", r, "\n")
}
cat("bad rows found by the SKILL's awk check (NF != 9), cut6.gtf:", length(which(vapply(strsplit(readLines("cut6.gtf"), "\t"), length, 1L) != 9)), "of", length(readLines("cut6.gtf")), "\n")
r <- tryCatch({ x <- prepareAnnotations("F:/OpenScience/audits/bio-long-read-splicing/run/data/plant/ref.gtf"); paste("good GTF ok,", length(x), "transcripts") }, error = function(e) conditionMessage(e))
cat(r, "\n")
