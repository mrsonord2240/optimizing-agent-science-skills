# Batch-design Input 1 (Canonical, regression of pre-fix Input 1): 24 plasma samples
# (12 case / 12 control, sex balanced) into 3 LC-MS batches of 8. SKILL.md constrained-assignment
# block (b02_assign) run verbatim, now followed by the NEW verification block (b02_verify) added
# by the fix. SYNTHETIC design.
.libPaths(c('F:/OpenScience/audit-envs/untargeted-metabolomics-analyst/R-lib', .libPaths()))
set.seed(915)
BB <- 'F:/OpenScience/audits/bio-experimental-design-batch-design'

run_block <- function(path) {
  tryCatch({
    withCallingHandlers(sys.source(path, envir = globalenv()),
      warning = function(w) { cat('  [warning]', conditionMessage(w), '\n'); invokeRestart('muffleWarning') })
    'OK'
  }, error = function(e) paste('ERROR:', conditionMessage(e)))
}

res1 <- run_block(file.path(BB, 'runs', 'blocks', 'b02_assign.R'))
cat('[b02_assign]', res1, '| designit', as.character(packageVersion('designit')), '\n')
if (exists('assignment')) {
  a <- as.data.frame(assignment); print(head(a, 3))
  cat('empty positions:', sum(is.na(a$id)), '\n')
}

res2 <- run_block(file.path(BB, 'runs', 'blocks', 'b02_verify.R'))
cat('[b02_verify]', res2, '\n')
