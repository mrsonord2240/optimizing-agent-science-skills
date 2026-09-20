suppressPackageStartupMessages(library(IsoformSwitchAnalyzeR))
src <- deparse(IsoformSwitchAnalyzeR::analyzePFAM)
cat(src[95:140], sep = "\n")
