.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({
  library(Signac)
  library(EnsDb.Hsapiens.v86)
})

cat('--- Source of GetGRangesFromEnsDb (checking for biovizBase dependency) ---\n')
fn <- Signac::GetGRangesFromEnsDb
print(fn)

cat('\n--- Does biovizBase appear in Signac DESCRIPTION as Imports/Suggests? ---\n')
desc <- read.dcf(system.file('DESCRIPTION', package = 'Signac'))
print(desc[, intersect(colnames(desc), c('Imports','Suggests','Depends'))])

cat('\n--- Simulate biovizBase genuinely unavailable: call with biovizBase namespace forcibly blocked ---\n')
# Temporarily shadow requireNamespace to simulate biovizBase not installed and see what GetGRangesFromEnsDb does
orig_requireNamespace <- base::requireNamespace
trace_env <- new.env()
result <- tryCatch({
  # Use a fake package name search override via .Options is fragile; instead directly test the
  # documented real-world symptom: uninstalling is destructive, so verify via getAnywhere/body scan
  # for an explicit requireNamespace('biovizBase') guard, which is the actual mechanism.
  body_txt <- paste(deparse(body(fn)), collapse = '\n')
  if (grepl('biovizBase', body_txt)) 'GUARD_FOUND_IN_BODY' else 'NO_DIRECT_GUARD_IN_TOP_LEVEL_BODY'
}, error = function(e) paste('ERROR:', conditionMessage(e)))
cat('Result:', result, '\n')

cat('\n--- Grep fixed SKILL.md + usage-guide.md for any Rsamtools reference ---\n')
skill_txt <- paste(readLines('F:/OpenScience/wt/sc-atac/single-cell/scatac-analysis/SKILL.md'), collapse = '\n')
guide_txt <- paste(readLines('F:/OpenScience/wt/sc-atac/single-cell/scatac-analysis/usage-guide.md'), collapse = '\n')
cat('SKILL.md mentions Rsamtools:', grepl('Rsamtools', skill_txt), '\n')
cat('usage-guide.md mentions Rsamtools:', grepl('Rsamtools', guide_txt), '\n')
cat('SKILL.md mentions bgzip/tabix:', grepl('bgzip|tabix', skill_txt, ignore.case = TRUE), '\n')
cat('usage-guide.md mentions bgzip/tabix:', grepl('bgzip|tabix', guide_txt, ignore.case = TRUE), '\n')
cat('DONE\n')
