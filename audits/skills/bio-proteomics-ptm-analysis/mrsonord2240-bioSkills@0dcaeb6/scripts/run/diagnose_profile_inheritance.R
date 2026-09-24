runtime <- file.path(R.home("bin"), "Rscript.exe")
child <- "F:/OpenScience/audits/bio-proteomics-ptm-analysis/run/diagnose_msstatsptm_profile.R"
status <- system2(runtime, child)
cat("child_status=", status, "\n", sep = "")
if (!identical(status, 0L)) quit(save = "no", status = status)
