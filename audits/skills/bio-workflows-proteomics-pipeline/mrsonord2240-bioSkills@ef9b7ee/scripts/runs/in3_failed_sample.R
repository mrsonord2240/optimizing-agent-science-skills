# Pipeline Input 3 (edge): T4 loaded ~3x low (proteinGroups_failed.txt) -> SKILL.md "Complete R Workflow" block run verbatim. SYNTHETIC data.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
PP <- 'F:/OpenScience/audits/bio-workflows-proteomics-pipeline'
setwd(file.path(PP, 'runs', 'work3')); set.seed(1)
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
raw2 <- read.delim('proteinGroups.txt', stringsAsFactors = FALSE)
R2 <- raw2[raw2$Reverse != '+' & raw2$Potential.contaminant != '+' & raw2$Only.identified.by.site != '+', ]
for (fam in c('Intensity.', 'LFQ.intensity.')) {
  M <- as.matrix(R2[, grep(paste0('^', fam, '[CT][0-9]$'), names(R2))]); M[M == 0] <- NA; L <- log2(M)
  cat(sprintf('%-15s raw medians: %s | ID counts: %s\n', fam, paste(round(apply(L, 2, median, na.rm = TRUE), 2), collapse = ' '), paste(colSums(!is.na(L)), collapse = ' ')))
}
cat('failed samples flagged by the block rule (<50% of median ID count):', if (exists('failed')) paste(failed, collapse = ',') else 'n/a', '\n')
