.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# Re-audit 2026-09-15, Input 4: SKILL.md decision-tree row, MSstatsTMT dataProcessPlotsTMT only after
# proteinSummarization(..., global_norm = FALSE, reference_norm = FALSE). SYNTHETIC protein-level table ->
# one pseudo-PSM per protein (the row states PSM-level input is needed). Compare with the default global_norm = TRUE.
suppressPackageStartupMessages({library(MSstatsTMT); library(data.table)})
cat('MSstatsTMT', as.character(packageVersion('MSstatsTMT')), '\n')
D <- 'F:/OpenScience/audits/bio-proteomics-proteomics-qc/data'
OUT <- 'F:/OpenScience/audits/bio-proteomics-proteomics-qc/rerun/out_in4'
dir.create(OUT, showWarnings = FALSE)
des <- fread(file.path(D, 'tmt_design.csv'), colClasses = 'character')
rows <- list()
for (p in c('A', 'B')) {
  m <- fread(file.path(D, sprintf('tmt_plex%s.csv', p)), colClasses = list(character = 'protein'))
  long <- melt(m, id.vars = 'protein', variable.name = 'Channel', value.name = 'Intensity')
  long[, Channel := as.character(Channel)]
  long <- merge(long, des[plex == p], by.x = 'Channel', by.y = 'channel')
  long[, `:=`(ProteinName = protein, PeptideSequence = paste0('PEP', protein), Charge = 2L,
              PSM = paste0('PEP', protein, '_2'), Mixture = paste0('Mix', p), TechRepMixture = 1L,
              Run = paste0('Run', p), Condition = ifelse(condition == 'Reference', 'Norm', condition),
              BioReplicate = ifelse(condition == 'Reference', 'Norm', sample))]
  rows[[p]] <- long[, .(ProteinName, PeptideSequence, Charge, PSM, Mixture, TechRepMixture, Run, Channel, Condition, BioReplicate, Intensity)]
}
psm <- rbindlist(rows)
med <- function(s) as.data.table(s$FeatureLevelData)[, .(med = round(median(log2Intensity, na.rm = TRUE), 2)), by = .(Mixture, Channel)]
s_off <- proteinSummarization(psm, method = 'msstats', global_norm = FALSE, reference_norm = FALSE, use_log_file = FALSE)
s_def <- proteinSummarization(psm, method = 'msstats', use_log_file = FALSE)
a <- med(s_off); b <- med(s_def)
cat('global_norm=FALSE, reference_norm=FALSE: channel median log2 range by mixture\n'); print(a[, .(min = min(med), max = max(med)), by = Mixture])
cat('defaults (global_norm=TRUE): channel median log2 range by mixture\n'); print(b[, .(min = min(med), max = max(med)), by = Mixture])
r <- tryCatch({dataProcessPlotsTMT(data = s_off, type = 'QCPlot', which.Protein = 'allonly', address = file.path(OUT, 'noNorm_')); 'ok'},
              error = function(e) paste('ERROR', conditionMessage(e)))
cat('dataProcessPlotsTMT QCPlot:', r, '\n'); print(list.files(OUT))
