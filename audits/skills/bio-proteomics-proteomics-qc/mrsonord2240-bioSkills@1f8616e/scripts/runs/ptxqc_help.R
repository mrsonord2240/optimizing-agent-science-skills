.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# Look up PTXQC's own help text for the contaminant metrics (verifies SKILL.md "PTXQC default flags >1%").
suppressPackageStartupMessages(library(PTXQC))
for (nm in c('qcMetric_EVD_UserContaminant', 'qcMetric_PG_Cont', 'qcMetric_EVD_Contaminants', 'qcMetric_SM_MSMSIdRate', 'qcMetric_MSMS_MissedCleavages')) {
  obj <- tryCatch(get(nm, envir = asNamespace('PTXQC')), error = function(e) NULL)
  cat('=====', nm, if (is.null(obj)) 'NOT FOUND' else '', '\n')
  if (!is.null(obj)) { o <- obj$new(); cat(o$helpText, '\n') }
}
cat(grep('^qcMetric_', ls(asNamespace('PTXQC')), value = TRUE), sep = '\n')
