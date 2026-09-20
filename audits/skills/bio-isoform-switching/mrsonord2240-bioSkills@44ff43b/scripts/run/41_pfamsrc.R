suppressPackageStartupMessages(library(IsoformSwitchAnalyzeR))
src <- deparse(IsoformSwitchAnalyzeR::analyzePFAM)
i <- grep("read|domtbl|pfam_scan|seq id|hmmscan|Web|web|local|header|col", src, ignore.case = TRUE)
cat(src[sort(unique(i))][1:70], sep="\n")
