.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
Sys.setenv(RSTUDIO_PANDOC='F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/tools/pandoc/pandoc-3.11')
suppressPackageStartupMessages(library(PTXQC))
D <- 'F:/OpenScience/audits/bio-proteomics-proteomics-qc/rerun2/qc2'
cat('--- B: same call, RSTUDIO_PANDOC set to Pandoc 3.11 ---\n')
cat('pandoc_available():', rmarkdown::pandoc_available(),
    '| version:', as.character(rmarkdown::pandoc_version()), '\n')
t0 <- Sys.time()
r <- createReport(txt_folder = D)
cat('elapsed min', round(as.numeric(difftime(Sys.time(), t0, units='mins')), 2), '\n')
print(list.files(D))
cat('HTML exists:', file.exists(r$report_file_HTML),
    '| size kB:', round(file.size(r$report_file_HTML)/1024, 1), '\n')
cat('PDF  exists:', file.exists(r$report_file_PDF),
    '| size kB:', round(file.size(r$report_file_PDF)/1024, 1), '\n')
cat('mzQC exists:', file.exists(r$mzQC_file), '\n')
# --- the heatmap scores the Skill's decision-tree row promises ("per-metric scores in [0,1], QC heatmap") ---
hm <- read.delim(r$heatmap_values_file, check.names = FALSE)
cat('\nheatmap dims:', paste(dim(hm), collapse=' x '), '\n')
print(names(hm))
print(hm)
