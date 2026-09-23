.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# Input 4: SKILL.md routes TMT channel balance to MSstatsTMT dataProcessPlotsTMT() "on RAW reporter intensities".
# The SYNTHETIC input is protein-level; MSstatsTMT needs PSM-level rows, so each protein becomes one pseudo-PSM.
suppressPackageStartupMessages({library(MSstatsTMT); library(data.table)})
cat('MSstatsTMT', as.character(packageVersion('MSstatsTMT')), '\n')
print(args(dataProcessPlotsTMT))
D <- 'F:/OpenScience/audits/bio-proteomics-proteomics-qc/data'
OUT <- 'F:/OpenScience/audits/bio-proteomics-proteomics-qc/runs/out_in4'
dir.create(OUT, showWarnings = FALSE)
des <- fread(file.path(D, 'tmt_design.csv'), colClasses = 'character')
rows <- list()
for (p in c('A', 'B')) {
  m <- fread(file.path(D, sprintf('tmt_plex%s.csv', p)), colClasses = list(character = 'protein'))
  long <- melt(m, id.vars = 'protein', variable.name = 'Channel', value.name = 'Intensity')
  long[, Channel := as.character(Channel)]
  d <- des[plex == p]
  long <- merge(long, d, by.x = 'Channel', by.y = 'channel')
  long[, `:=`(ProteinName = protein, PeptideSequence = paste0('PEP', protein), Charge = 2L,
              PSM = paste0('PEP', protein, '_2'), Mixture = paste0('Mix', p), TechRepMixture = 1L,
              Run = paste0('Run', p), Condition = ifelse(condition == 'Reference', 'Norm', condition),
              BioReplicate = ifelse(condition == 'Reference', 'Norm', sample))]
  rows[[p]] <- long[, .(ProteinName, PeptideSequence, Charge, PSM, Mixture, TechRepMixture, Run, Channel, Condition, BioReplicate, Intensity)]
}
psm <- rbindlist(rows)
cat('pseudo-PSM rows', nrow(psm), '\n')
summ <- tryCatch(proteinSummarization(psm, method = 'msstats', global_norm = TRUE, reference_norm = TRUE,
                                      remove_norm_channel = TRUE, use_log_file = FALSE),
                 error = function(e) { cat('proteinSummarization ERROR:', conditionMessage(e), '\n'); NULL })
if (!is.null(summ)) {
  cat('summarized proteins', length(unique(summ$ProteinLevelData$Protein)), '\n')
  r <- tryCatch(dataProcessPlotsTMT(data = summ, type = 'QCPlot', which.Protein = 'allonly',
                                    address = file.path(OUT, 'tmt_')),
                error = function(e) { cat('dataProcessPlotsTMT ERROR:', conditionMessage(e), '\n'); NULL })
  print(list.files(OUT))
  # channel medians on log2 raw feature intensities vs after global+reference normalisation
  fl <- as.data.table(summ$FeatureLevelData)
  print(fl[, .(median_log2_feature = round(median(log2Intensity, na.rm = TRUE), 2)), by = .(Mixture, Channel)][order(Mixture, Channel)])
  pl <- as.data.table(summ$ProteinLevelData)
  print(pl[, .(median_protein_abund = round(median(Abundance, na.rm = TRUE), 2)), by = .(Mixture, Channel)][order(Mixture, Channel)])
}
