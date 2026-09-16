# Batch-design Input 1 (canonical): 24 plasma samples (12 case / 12 control, sex balanced) into 3 LC-MS batches of 8.
# SKILL.md constrained-assignment block run verbatim (its example data frame matches this design). SYNTHETIC design.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
set.seed(915)
BB <- 'F:/OpenScience/audits/bio-experimental-design-batch-design'
blk <- list.files(file.path(BB, 'runs', 'blocks'), pattern = '^b02', full.names = TRUE)
res <- tryCatch({ withCallingHandlers(suppressMessages(sys.source(blk, envir = globalenv())),
  warning = function(w) { cat('  [warning]', conditionMessage(w), '\n'); invokeRestart('muffleWarning') }); 'OK' },
  error = function(e) paste('ERROR:', conditionMessage(e)))
cat('[designit block verbatim]', res, '| designit', as.character(packageVersion('designit')), '\n')
if (exists('assignment')) {
  a <- as.data.frame(assignment); print(head(a, 3))
  cat('condition x batch:\n'); print(table(a$condition, a$batch)); cat('sex x batch:\n'); print(table(a$sex, a$batch))
  cat('empty positions:', sum(is.na(a$id)), '\n')
}
