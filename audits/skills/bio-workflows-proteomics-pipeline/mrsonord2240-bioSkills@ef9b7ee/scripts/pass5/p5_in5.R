# RE-AUDIT Input 5 (stress): MaxQuant evidence -> fixed SKILL.md "MSstats Workflow" block, verbatim. SYNTHETIC data.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
PP <- 'F:/OpenScience/audits/bio-workflows-proteomics-pipeline'
setwd(file.path(PP, 'pass5', 'work5'))
blk <- list.files(file.path(PP, 'pass5', 'blocks'), pattern = '^b02', full.names = TRUE)
res <- tryCatch({ withCallingHandlers(sys.source(blk, envir = globalenv()),
  warning = function(w) { cat('  [warning]', substr(conditionMessage(w), 1, 140), '\n'); invokeRestart('muffleWarning') }); 'OK' },
  error = function(e) paste('ERROR:', conditionMessage(e)))
cat('[MSstats block verbatim]', res, '\n')
cat('evidence rows read:', nrow(evidence), '| data lines in file:', length(readLines('evidence.txt')) - 1,
    '| proteinGroups rows:', nrow(proteinGroups), '| lines:', length(readLines('proteinGroups.txt')) - 1, '\n')
if (exists('processed')) cat('proteins summarized:', length(unique(processed$ProteinLevelData$Protein)), '\n')
if (exists('results')) {
  r <- results$ComparisonResult
  truth <- read.csv(file.path(PP, 'data', 'truth_proteins.csv'), na.strings = character(0))
  tested <- as.character(r$Protein)
  cls_all <- truth$class[match(tested, truth$protein)]
  cat('proteins in ComparisonResult:', length(tested),
      '| of which true nulls:', sum(cls_all == 'null', na.rm = TRUE),
      '| up:', sum(cls_all == 'up', na.rm = TRUE),
      '| down:', sum(cls_all == 'down', na.rm = TRUE),
      '| on_off:', sum(cls_all == 'on_off', na.rm = TRUE), '\n')
  s <- tested[!is.na(r$adj.pvalue) & r$adj.pvalue < 0.05]
  cl <- truth$class[match(s, truth$protein)]
  cat('adj.p<0.05 called:', length(s), '| FALSE POSITIVES (true nulls):', sum(cl == 'null', na.rm = TRUE),
      '| true up:', sum(cl == 'up', na.rm = TRUE), '| true down:', sum(cl == 'down', na.rm = TRUE),
      '| on_off:', sum(cl == 'on_off', na.rm = TRUE), '\n')
  nulls_tested <- sum(cls_all == 'null', na.rm = TRUE)
  cat(sprintf('observed null-calling rate at BH 0.05: %d/%d = %.1f%%\n',
      sum(cl == 'null', na.rm = TRUE), nulls_tested, 100*sum(cl=='null',na.rm=TRUE)/nulls_tested))
  # raw-p calibration of the nulls: is the p-value distribution itself miscalibrated?
  pn <- r$pvalue[cls_all == 'null' & !is.na(r$pvalue)]
  cat(sprintf('true nulls with raw p<0.05: %d/%d = %.1f%% (nominal 5%%)\n', sum(pn<0.05), length(pn), 100*mean(pn<0.05)))
  cat(sprintf('true nulls with raw p<0.01: %d/%d = %.1f%% (nominal 1%%)\n', sum(pn<0.01), length(pn), 100*mean(pn<0.01)))
  write.csv(r, 'msstats_comparison.csv', row.names = FALSE)
}
