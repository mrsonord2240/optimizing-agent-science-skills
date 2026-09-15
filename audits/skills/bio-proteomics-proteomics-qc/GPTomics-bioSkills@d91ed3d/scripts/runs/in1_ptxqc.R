.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# Input 1: SKILL.md Decision Tree row 1 -> PTXQC createReport(txt_folder=...) on a MaxQuant txt/ folder.
# Folder holds only the SYNTHETIC proteinGroups.txt + evidence.txt (no summary/parameters/msms/msmsScans).
suppressPackageStartupMessages(library(PTXQC))
cat('PTXQC', as.character(packageVersion('PTXQC')), '\n')
txt <- 'F:/OpenScience/audits/bio-proteomics-proteomics-qc/data/ptxqc_txt'
t0 <- Sys.time()
r <- tryCatch(createReport(txt_folder = txt), error = function(e) { cat('ERROR:', conditionMessage(e), '\n'); NULL })
cat('elapsed', format(Sys.time() - t0), '\n')
if (!is.null(r)) print(r)
print(list.files(txt, recursive = TRUE))
