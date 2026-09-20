pk <- c("IsoformSwitchAnalyzeR","DRIMSeq","DEXSeq","satuRn","stageR","fishpond","tximport","tximeta","DESeq2","BiocParallel")
for (p in pk) cat(p, as.character(packageVersion(p)), "\n")
cat(R.version.string, "\n")
library(IsoformSwitchAnalyzeR)
show <- function(f) { cat("\n==", f, "==\n"); print(names(formals(get(f)))) }
for (f in c("importIsoformExpression","importRdata","preFilter","isoformSwitchTestSatuRn","isoformSwitchTestDEXSeq","extractSequence","analyzeORF","analyzeCPC2","analyzePFAM","analyzeSignalP","analyzeIUPred2A","analyzeAlternativeSplicing","analyzeSwitchConsequences","extractTopSwitches","switchPlot","extractConsequenceSummary","extractConsequenceEnrichment","extractSplicingSummary","extractSwitchSummary")) {
  if (exists(f)) show(f) else cat("\nMISSING:", f, "\n")
}
