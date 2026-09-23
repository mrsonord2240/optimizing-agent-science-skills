# Pipeline Input 1 (canonical): MaxQuant LFQ 4 v 4 with batch -> SKILL.md "Complete R Workflow" block run verbatim. SYNTHETIC data.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
PP <- 'F:/OpenScience/audits/bio-workflows-proteomics-pipeline'
setwd(file.path(PP, 'runs', 'work1')); set.seed(1)
blk <- list.files(file.path(PP, 'runs', 'blocks'), pattern = '^b01', full.names = TRUE)
res <- tryCatch({ withCallingHandlers(sys.source(blk, envir = globalenv()),
  warning = function(w) { cat('  [warning]', conditionMessage(w), '\n'); invokeRestart('muffleWarning') }); 'OK' },
  error = function(e) paste('ERROR:', conditionMessage(e)))
cat('[Complete R Workflow block verbatim]', res, '\n')
raw <- read.delim('proteinGroups.txt', stringsAsFactors = FALSE)
cat('flag columns classes:', class(raw$Reverse), class(raw$Potential.contaminant), class(raw$Only.identified.by.site), '\n')
if (exists('proteins')) cat('rows after the block filter:', nrow(proteins), '| all-NA rows (NA-subset artefacts):', sum(is.na(proteins$Protein.IDs)), '| REV/CON left:', sum(grepl('^(REV__|CON__)', proteins$Protein.IDs)), '\n')
if (exists('results')) {
  truth <- read.csv(file.path(PP, 'data', 'truth_proteins.csv'), na.strings = character(0))
  id <- sub(';.*', '', results$protein); cls <- truth$class[match(id, truth$protein)]
  s <- results$significant
  cat(sprintf('treat(1.5-fold) BH<0.05 on imputed data: %d called | null %d | on_off %d | up %d | down %d | unmatched ids %d\n', sum(s), sum(cls[s] == 'null', na.rm = TRUE),
      sum(cls[s] == 'on_off', na.rm = TRUE), sum(cls[s] == 'up', na.rm = TRUE), sum(cls[s] == 'down', na.rm = TRUE), sum(is.na(cls[s]))))
  cat('design columns:', colnames(design), '| batch in design:', any(grepl('batch', colnames(design))), '\n')
}
