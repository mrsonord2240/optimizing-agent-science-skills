# Batch-design Input 2 (Variant A, regression of pre-fix Input 2): 60 plasma samples
# (30 case / 30 ctrl, 3 sites) into 4 TMTpro 16plex plexes with a pooled reference in channel 16
# of every plex. Pre-fix, the Skill gave no bridge-channel code and the agent had to adapt the
# generic assignment block (P2 finding). Post-fix, SKILL.md's new "Reference / Bridge Channel
# Layout" section (b03_bridge) is run VERBATIM -- no agent adaptation needed. SYNTHETIC design.
.libPaths(c('F:/OpenScience/audit-envs/untargeted-metabolomics-analyst/R-lib', .libPaths()))
set.seed(16)
BB <- 'F:/OpenScience/audits/bio-experimental-design-batch-design'
t0 <- Sys.time()
res <- tryCatch({
  withCallingHandlers(sys.source(file.path(BB, 'runs', 'blocks', 'b03_bridge.R'), envir = globalenv()),
    warning = function(w) { cat('  [warning]', conditionMessage(w), '\n'); invokeRestart('muffleWarning') })
  'OK'
}, error = function(e) paste('ERROR:', conditionMessage(e)))
cat('[b03_bridge verbatim]', res, '| designit', as.character(packageVersion('designit')),
    '| elapsed s:', round(as.numeric(difftime(Sys.time(), t0, units = 'secs')), 1), '\n')
if (exists('assignment')) {
  a <- assignment
  cat('condition x plex:\n'); print(table(a$condition, a$plex))
  cat('site x plex:\n'); print(table(a$site, a$plex))
  cat('positions per plex used:', paste(table(a$plex[!is.na(a$id)]), collapse = ','), '\n')
}
