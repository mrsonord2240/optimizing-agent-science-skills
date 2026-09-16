.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
Sys.setenv(RSTUDIO_PANDOC='F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/tools/pandoc/pandoc-3.11')
# Re-audit batch C, Input 2 (NEW). The Skill's thesis is "the matrix sees the failure last" and it routes
# Level-2/3 QC to PTXQC createReport(). Question: with the report path now complete (Pandoc 3.11), does
# PTXQC's own report flag a run that is a 0.39x loading failure? SYNTHETIC txt/ folder from make_failed_txt.py.
suppressPackageStartupMessages(library(PTXQC))
D <- 'F:/OpenScience/audits/bio-proteomics-proteomics-qc/rerun2/qc_failed'
cat('pandoc_available():', rmarkdown::pandoc_available(), '\n')
r <- createReport(txt_folder = D)
cat('HTML:', file.exists(r$report_file_HTML), '| PDF:', file.exists(r$report_file_PDF),
    '| mzQC:', file.exists(r$mzQC_file), '\n')
hm <- read.delim(r$heatmap_values_file, check.names = FALSE)
names(hm) <- gsub('EVD:~|MSMS:~|~\\\[[0-9]+\]\\|\\|~', ' ', names(hm))
cat('\n--- PTXQC per-run heatmap scores (1 = best) ---\n')
print(format(hm, digits = 3), row.names = FALSE)
cat('\n--- which run has the worst Average Overall Quality? ---\n')
q <- hm[[ncol(hm)]]; names(q) <- hm[[1]]
print(round(sort(q), 4))
cat('T4 rank (1 = worst):', which(names(sort(q)) == 'T4'), 'of', length(q), '\n')
