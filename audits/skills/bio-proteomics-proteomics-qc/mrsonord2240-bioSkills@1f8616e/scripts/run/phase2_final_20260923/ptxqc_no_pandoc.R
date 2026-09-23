.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# Fresh Phase 2 audit: exact createReport(txt_folder=...) call without Pandoc available.
suppressPackageStartupMessages(library(PTXQC))
folder <- 'F:/OpenScience/audits/bio-proteomics-proteomics-qc/run/phase2_final_20260923/ptxqc_no_pandoc'
cat('PTXQC=', as.character(packageVersion('PTXQC')), ' rmarkdown=', as.character(packageVersion('rmarkdown')), '\n', sep='')
cat('pandoc_available=', rmarkdown::pandoc_available(), '\n', sep='')
result <- createReport(txt_folder=folder)
cat('pdf_exists=', file.exists(result$report_file_PDF), ' html_exists=', file.exists(result$report_file_HTML),
    ' mzqc_exists=', file.exists(result$mzQC_file), '\n', sep='')
heatmap <- read.delim(result$heatmap_values_file, check.names=FALSE)
cat('heatmap_dims=', paste(dim(heatmap), collapse='x'), '\n', sep='')
