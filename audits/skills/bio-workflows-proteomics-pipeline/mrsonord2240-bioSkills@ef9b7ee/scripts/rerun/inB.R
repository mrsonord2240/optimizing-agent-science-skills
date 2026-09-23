
# RE-AUDIT new Input B: does the %in% flag-column filter hold for BOTH the all-empty and the mixed case?
# The fixed "Complete R Workflow" block is run VERBATIM on each. SYNTHETIC data (rerun/make_flagcases.py).
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
PP <- 'F:/OpenScience/audits/bio-workflows-proteomics-pipeline'
blk <- list.files(file.path(PP, 'rerun', 'blocks'), pattern = '^b01', full.names = TRUE)
for (w in c('workB1', 'workB2')) {
  setwd(file.path(PP, 'rerun', w))
  cat('\n========================= ', w, '\n')
  raw <- read.delim('proteinGroups.txt', stringsAsFactors = FALSE, quote = '', comment.char = '')
  cat('flag column classes as read.delim types them:',
      paste(sapply(raw[, c('Reverse','Potential.contaminant','Only.identified.by.site')], class), collapse = ' '), '\n')
  truly_flagged <- sum(raw$Reverse %in% '+' | raw$Potential.contaminant %in% '+' | raw$Only.identified.by.site %in% '+')
  cat('rows in file:', nrow(raw), '| rows genuinely flagged:', truly_flagged, '| expected to survive:', nrow(raw) - truly_flagged, '\n')
  # the PRE-FIX predicate, for comparison
  old <- tryCatch(nrow(raw[raw$Potential.contaminant != '+' & raw$Reverse != '+' & raw$Only.identified.by.site != '+', ]),
                  error = function(e) paste('ERROR', conditionMessage(e)))
  oldsub <- tryCatch(raw[raw$Potential.contaminant != '+' & raw$Reverse != '+' & raw$Only.identified.by.site != '+', ],
                     error = function(e) NULL)
  cat('PRE-FIX (!= plus-sign) predicate: nrow =', old, '| all-NA rows produced:',
      if (is.null(oldsub)) NA else sum(is.na(oldsub$Protein.IDs)), '\n')
  e <- new.env(parent = globalenv())
  r <- tryCatch({ suppressWarnings(suppressMessages(capture.output(sys.source(blk, envir = e)))); 'OK' },
                error = function(z) paste('ERROR:', conditionMessage(z)))
  cat('[fixed block verbatim]', r, '\n')
  if (exists('proteins', envir = e)) {
    p <- get('proteins', envir = e)
    cat('FIXED predicate: nrow =', nrow(p), '| all-NA rows:', sum(is.na(p$Protein.IDs)),
        '| flagged rows left in:', sum(p$Reverse %in% '+' | p$Potential.contaminant %in% '+' | p$Only.identified.by.site %in% '+'),
        '| CORRECT:', nrow(p) == nrow(raw) - truly_flagged && sum(is.na(p$Protein.IDs)) == 0, '\n')
  }
  if (exists('results', envir = e)) {
    res <- get('results', envir = e)
    cat('pipeline completed: proteins tested', nrow(res), '| significant', sum(res$significant), '\n')
  }
}
