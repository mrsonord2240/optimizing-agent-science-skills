.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# Re-audit 2026-09-15, Input 1: SKILL.md decision-tree row "PTXQC createReport(txt_folder=...)" on the SYNTHETIC txt folder.
suppressPackageStartupMessages(library(PTXQC))
cat('PTXQC', as.character(packageVersion('PTXQC')), '\n')
t0 <- Sys.time()
r <- tryCatch(createReport(txt_folder = 'F:/OpenScience/audits/bio-proteomics-proteomics-qc/rerun/ptxqc_txt'), error = function(e) paste('ERROR', conditionMessage(e)))
cat('elapsed min', round(as.numeric(difftime(Sys.time(), t0, units = 'mins')), 2), '\n')
print(r)
print(list.files('F:/OpenScience/audits/bio-proteomics-proteomics-qc/rerun/ptxqc_txt', recursive = TRUE))
