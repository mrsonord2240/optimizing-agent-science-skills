# Confirm root cause: MetaboAnalystR's AddErrMsg() does current.msg <<- c(current.msg, msg),
# which requires 'current.msg' and 'err.vec' to already exist in globalenv (normally set up by
# the Shiny web app's .init.global.vars(), never by a plain `library(MetaboAnalystR)` session).
current.msg <- character(0)
err.vec <- character(0)
suppressMessages(library(MetaboAnalystR))
setwd("F:/OpenScience/audits/bio-metabolomics-pathway-mapping/run")
mSet <- InitDataObjects('mass_all', 'mummichog', FALSE)
mSet <- SetPeakFormat(mSet, 'mpt')
mSet <- UpdateInstrumentParameters(mSet, 5.0, 'negative')
mSet <- Read.PeakListData(mSet, "F:/OpenScience/audits/bio-metabolomics-pathway-mapping/data/input2b_peaks_significant_only_synthetic.csv")
res <- tryCatch({
  mSet <- SanityCheckMummichogData(mSet)
  "OK"
}, error = function(e) paste("R ERROR:", conditionMessage(e)))
cat("SanityCheckMummichogData result:", res, "\n")
cat("Actual diagnostic message once current.msg/err.vec pre-exist:", paste(current.msg, collapse=" | "), "\n")
