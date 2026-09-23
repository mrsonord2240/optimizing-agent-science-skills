.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# Re-audit 2026-09-15 batch C, Input 1: the SKILL.md decision-tree row
# "MaxQuant txt/ folder, want fast multi-metric report -> PTXQC createReport(txt_folder=...)"
# run BOTH ways: (A) exactly as the Skill writes it, in a clean session; (B) after pointing R at the
# newly installed Pandoc 3.11. SYNTHETIC MaxQuant txt/ folder (data/evidence.txt, data/proteinGroups.txt).
suppressPackageStartupMessages(library(PTXQC))
D <- 'F:/OpenScience/audits/bio-proteomics-proteomics-qc/pass5/qcA'
cat('PTXQC', as.character(packageVersion('PTXQC')),
    '| rmarkdown', as.character(packageVersion('rmarkdown')), '\n')
cat('--- A: verbatim, no environment change ---\n')
cat('rmarkdown::pandoc_available():', rmarkdown::pandoc_available(), '\n')
cat('Sys.which("pandoc"):', Sys.which('pandoc'), '\n')
t0 <- Sys.time()
r <- tryCatch(createReport(txt_folder = D), error = function(e) paste('ERROR', conditionMessage(e)))
cat('elapsed min', round(as.numeric(difftime(Sys.time(), t0, units='mins')), 2), '\n')
cat('files produced:\n'); print(list.files(D))
cat('HTML promised at:', r$report_file_HTML, '| exists:', file.exists(r$report_file_HTML), '\n')
cat('PDF  promised at:', r$report_file_PDF,  '| exists:', file.exists(r$report_file_PDF), '\n')
