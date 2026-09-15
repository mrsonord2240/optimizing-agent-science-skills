.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages(library(MSstats)); f <- formals(dataProcess); cat('dataProcess use_log_file default:', deparse(f$use_log_file), '\n'); f2 <- formals(MaxQtoMSstatsFormat); cat('MaxQtoMSstatsFormat use_log_file default:', deparse(f2$use_log_file), '\n')
