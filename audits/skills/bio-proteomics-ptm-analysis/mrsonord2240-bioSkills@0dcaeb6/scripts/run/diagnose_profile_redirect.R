runtime <- file.path(R.home("bin"), "Rscript.exe")
child <- "F:/OpenScience/audits/bio-proteomics-ptm-analysis/run/diagnose_msstatsptm_profile.R"
log <- tempfile(fileext = ".log")
status <- system2(runtime, child, stdout = log, stderr = log)
cat("child_status=", status, "\n", sep = "")
cat(readLines(log, warn = FALSE), sep = "\n")
if (!identical(status, 0L)) quit(save = "no", status = status)
