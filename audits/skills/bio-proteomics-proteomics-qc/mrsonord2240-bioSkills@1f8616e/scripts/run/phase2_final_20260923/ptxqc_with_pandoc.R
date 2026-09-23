.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# Fresh Phase 2 audit: same call with the documented RSTUDIO_PANDOC path.
Sys.setenv(RSTUDIO_PANDOC='F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/tools/pandoc/pandoc-3.11')
suppressPackageStartupMessages(library(PTXQC))
folder <- 'F:/OpenScience/audits/bio-proteomics-proteomics-qc/run/phase2_final_20260923/ptxqc_with_pandoc'
cat('pandoc_available=', rmarkdown::pandoc_available(), ' version=', as.character(rmarkdown::pandoc_version()), '\n', sep='')
result <- createReport(txt_folder=folder)
cat('pdf_exists=', file.exists(result$report_file_PDF), ' html_exists=', file.exists(result$report_file_HTML),
    ' mzqc_exists=', file.exists(result$mzQC_file), '\n', sep='')
cat('html_kb=', round(file.size(result$report_file_HTML)/1024, 1), '\n', sep='')
