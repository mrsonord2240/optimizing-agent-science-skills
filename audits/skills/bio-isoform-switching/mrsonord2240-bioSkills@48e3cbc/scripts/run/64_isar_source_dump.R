# Read the installed ISAR 2.6.0 wrapper source (deparse) to check what its q-values are and where the replicate warnings come from.
suppressPackageStartupMessages(library(IsoformSwitchAnalyzeR))
for (fn in c("isoformSwitchTestDEXSeq", "isoformSwitchTestSatuRn")) { s <- deparse(getFromNamespace(fn, "IsoformSwitchAnalyzeR"))
  cat("==", fn, ":", length(s), "lines\n"); cat(grep("replicates|round[(]|padj|DEXSeqResults|estimateSizeFactors", s, value = TRUE), sep = "\n") }
cat("importRdata detectUnwantedEffects default:", deparse(formals(importRdata)$detectUnwantedEffects), "\n")
