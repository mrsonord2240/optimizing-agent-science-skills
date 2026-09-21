# Does IsoformSwitchAnalyzeR 2.6.0 (installed) choose the DTU test automatically ANYWHERE? Read isoformSwitchAnalysisPart1's body, then RUN it on the
# 3v3 (should use DEXSeq if it follows "any condition > 5 replicates -> satuRn") and 6v6 (satuRn) planted+heterogeneity sets and record which test's message appears.
setwd("F:/OpenScience/audits/bio-isoform-switching/run/work"); source("../helpers.R")
suppressPackageStartupMessages(library(IsoformSwitchAnalyzeR)); cat("version", as.character(packageVersion("IsoformSwitchAnalyzeR")), "\n")
b <- deparse(body(isoformSwitchAnalysisPart1)); i <- grep("SatuRn|DEXSeq|nrReplicates", b); cat("Part1 lines mentioning the tests / replicates:", length(i), "\n"); cat(b[i], sep = "\n")
D <- "F:/OpenScience/audits/bio-isoform-switching/run/data"
# Part1 calls the tests with quiet = TRUE, so trace the two test functions to see which one it calls
ns <- asNamespace("IsoformSwitchAnalyzeR")
for (fn in c("isoformSwitchTestDEXSeq", "isoformSwitchTestSatuRn")) suppressMessages(trace(fn, tracer = bquote(cat("[TRACE]", .(fn), "called by isoformSwitchAnalysisPart1\n")), where = ns, print = FALSE))
for (nm in c("3v3", "6v6")) {
  src <- file.path(D, paste0("het_", nm)); wd <- paste0("w99_", nm); unlink(wd, recursive = TRUE); dir.create(wd); file.copy(file.path(src, c("salmon_quant", "annotation.gtf", "transcripts.fa", "sample_metadata.tsv")), wd, recursive = TRUE); setwd(wd)
  q <- importIsoformExpression("salmon_quant/", calculateCountsFromAbundance = FALSE, addIsofomIdAsColumn = TRUE, showProgress = FALSE, quiet = TRUE)
  meta <- read.delim("sample_metadata.tsv"); ids <- setdiff(colnames(q$counts), "isoform_id"); design <- data.frame(sampleID = ids, condition = meta$condition[match(ids, meta$sample_id)])
  sl <- suppressWarnings(importRdata(q$counts, q$abundance, design, "annotation.gtf", "transcripts.fa", addAnnotatedORFs = FALSE, showProgress = FALSE, quiet = TRUE))
  msgs <- character(); dir.create("p1out")
  sl2 <- withCallingHandlers(tryCatch(isoformSwitchAnalysisPart1(sl, pathToOutput = "p1out", pathToGTF = "annotation.gtf", outputSequences = FALSE, prepareForWebServers = FALSE, quiet = FALSE), error = function(e) { msgs <<- c(msgs, paste("ERROR:", conditionMessage(e))); NULL }),
     message = function(m) { msgs <<- c(msgs, conditionMessage(m)); invokeRestart("muffleMessage") }, warning = function(w) { msgs <<- c(msgs, paste("WARNING:", conditionMessage(w))); invokeRestart("muffleWarning") })
  cat(sprintf("[%s] replicates per condition: %s\n", nm, paste(names(table(design$condition)), table(design$condition), collapse = ", ")))
  cat("  messages naming the test:", paste(unique(grep("DEXSeq|satuRn|isoformSwitchTest", msgs, value = TRUE)), collapse = " || "), "\n")
  cat("  other Part1 messages:", paste(head(grep("Step|ERROR", msgs, value = TRUE), 6), collapse = " | "), "\n")
  if (!is.null(sl2)) cat("  isoformSwitchAnalysis has", nrow(sl2$isoformSwitchAnalysis), "rows; columns", paste(head(colnames(sl2$isoformSwitchAnalysis), 8), collapse = ","), "\n")
  setwd("..")
}
cat("DONE 99b\n")
