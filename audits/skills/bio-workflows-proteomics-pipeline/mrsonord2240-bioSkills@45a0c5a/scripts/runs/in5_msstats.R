# Pipeline Input 5 (stress): MaxQuant evidence -> SKILL.md "MSstats Workflow" block run verbatim. SYNTHETIC data.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
PP <- 'F:/OpenScience/audits/bio-workflows-proteomics-pipeline'
setwd(file.path(PP, 'runs', 'work5'))
blk <- list.files(file.path(PP, 'runs', 'blocks'), pattern = '^b02', full.names = TRUE)
res <- tryCatch({ withCallingHandlers(sys.source(blk, envir = globalenv()),
  warning = function(w) { cat('  [warning]', substr(conditionMessage(w), 1, 120), '\n'); invokeRestart('muffleWarning') }); 'OK' },
  error = function(e) paste('ERROR:', conditionMessage(e)))
cat('[MSstats block verbatim]', res, '\n')
cat('evidence rows read:', nrow(evidence), '| data lines in file:', length(readLines('evidence.txt')) - 1, '| proteinGroups rows:', nrow(proteinGroups), '| lines:', length(readLines('proteinGroups.txt')) - 1, '\n')
if (exists('processed')) cat('proteins summarized:', length(unique(processed$ProteinLevelData$Protein)), '\n')
if (exists('results')) { r <- results$ComparisonResult; truth <- read.csv(file.path(PP, 'data', 'truth_proteins.csv'), na.strings = character(0))
  s <- as.character(r$Protein[!is.na(r$adj.pvalue) & r$adj.pvalue < 0.05]); cl <- truth$class[match(s, truth$protein)]
  cat('groupComparison adj.p<0.05:', length(s), '| null:', sum(cl == 'null', na.rm = TRUE), '| proteins in truth set with evidence:', 300, '\n') }
