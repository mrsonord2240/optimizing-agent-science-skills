.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages(library(PTXQC))
o <- PTXQC:::qcMetric_EVD_Top5Cont$new(); cat(o$helpText, '\n')
