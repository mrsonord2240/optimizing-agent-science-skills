# Input 3 (Edge): user (mis)supplies ONLY significant features as the mummichog background,
# the exact "Common Errors" pitfall the SKILL.md's own table names first: "Everything is
# significant in mummichog | Input was significant features only, not R_all".
suppressMessages(library(MetaboAnalystR))
setwd("F:/OpenScience/audits/bio-metabolomics-pathway-mapping/run")

mSet <- InitDataObjects('mass_all', 'mummichog', FALSE)
mSet <- SetPeakFormat(mSet, 'mpt')
mSet <- UpdateInstrumentParameters(mSet, 5.0, 'negative')
mSet <- Read.PeakListData(mSet, "F:/OpenScience/audits/bio-metabolomics-pathway-mapping/data/input2b_peaks_significant_only_synthetic.csv")
mSet <- SanityCheckMummichogData(mSet)
mSet <- SetPeakEnrichMethod(mSet, 'mum', 'v2')
mSet <- SetMummichogPval(mSet, 0.2)
res <- tryCatch({
  mSet <- PerformPSEA(mSet, 'hsa_mfn', 'current', permNum = 200)
  "OK"
}, error = function(e) paste("ERROR:", conditionMessage(e)))
cat("PerformPSEA result:", res, "\n")
if (!is.null(mSet$mummi.resmat)) {
  df <- as.data.frame(mSet$mummi.resmat)
  cat("mummi.resmat dims:", dim(df), "\n")
  cat("Number of pathways with Gamma < 0.05:", sum(df$Gamma < 0.05, na.rm=TRUE), "of", nrow(df), "\n")
  print(df[order(df$Gamma), c("Pathway","Hits.sig","Expected","Gamma")])
} else {
  cat("mSet$mummi.resmat is NULL\n")
}
