# Input 2 (Variant A / canonical mummichog): full feature table as background (R_all),
# following bio-metabolomics-pathway-mapping SKILL.md pattern exactly.
suppressMessages(library(MetaboAnalystR))
setwd("F:/OpenScience/audits/bio-metabolomics-pathway-mapping/run")

mSet <- InitDataObjects('mass_all', 'mummichog', FALSE)
mSet <- SetPeakFormat(mSet, 'mpt')
mSet <- UpdateInstrumentParameters(mSet, 5.0, 'negative')
mSet <- Read.PeakListData(mSet, "F:/OpenScience/audits/bio-metabolomics-pathway-mapping/data/input2_peaks_full_synthetic.csv")
mSet <- SanityCheckMummichogData(mSet)
mSet <- SetPeakEnrichMethod(mSet, 'mum', 'v2')
mSet <- SetMummichogPval(mSet, 0.2)
res <- tryCatch({
  mSet <- PerformPSEA(mSet, 'hsa_mfn', 'current', permNum = 200)
  "OK"
}, error = function(e) paste("ERROR:", conditionMessage(e)))
cat("PerformPSEA result:", res, "\n")
if (!is.null(mSet$mummi.resmat)) {
  cat("mummi.resmat dims:", dim(mSet$mummi.resmat), "\n")
  print(head(as.data.frame(mSet$mummi.resmat), 10))
} else {
  cat("mSet$mummi.resmat is NULL\n")
}
