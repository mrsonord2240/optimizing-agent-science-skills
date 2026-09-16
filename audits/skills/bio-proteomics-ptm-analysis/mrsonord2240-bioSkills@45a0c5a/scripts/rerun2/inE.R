
# RE-AUDIT B, NEW PTM Input E (Scope / coverage): TMT11-plex phosphoproteomics with a pooled bridge
# channel. Can an agent following this SKILL.md actually get to a protein-adjusted result?
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages(library(MSstatsPTM))
cat('MSstatsPTM', as.character(packageVersion('MSstatsPTM')), '\n\n')
fns <- ls('package:MSstatsPTM')
cat('converters exported:', paste(grep('MSstatsPTMFormat$', fns, value = TRUE), collapse = ', '), '\n')
cat('all exported functions:', paste(fns, collapse = ', '), '\n\n')
cat('MaxQtoMSstatsPTMFormat args:\n  ', paste(names(formals(MaxQtoMSstatsPTMFormat)), collapse = ', '), '\n')
cat('  has a TMT/channel/plex argument:',
    any(grepl('tmt|channel|plex|reference|labeling', names(formals(MaxQtoMSstatsPTMFormat)), ignore.case = TRUE)),
    '| labeling_type default:', as.character(formals(MaxQtoMSstatsPTMFormat)$labeling_type), '\n\n')
cat('dataSummarizationPTM args:\n  ', paste(names(formals(dataSummarizationPTM)), collapse = ', '), '\n')
cat('groupComparisonPTM args:\n  ', paste(names(formals(groupComparisonPTM)), collapse = ', '), '\n')
cat('  data.type accepted values per the body:\n')
print(grep('data.type', deparse(body(groupComparisonPTM)), value = TRUE)[1:6])

# What does the SKILL.md say about TMT?
sk <- readLines('F:/OpenScience/external/mrsonord2240__bioSkills/proteomics/ptm-analysis/SKILL.md', warn = FALSE)
hits <- grep('\bTMT\b|isobaric label|reporter ion|bridge channel|reference channel|ratio compression|isolation interference|IRS',
             sk, ignore.case = TRUE)
cat('\nSKILL.md lines mentioning TMT / isobaric quant concepts:', length(hits), '\n')
for (h in hits) cat('  L', h, ': ', substr(trimws(sk[h]), 1, 150), '\n', sep = '')
cat('\nDecision Tree rows mentioning TMT:',
    length(grep('TMT', sk[grep('^## Decision Tree', sk):(grep('^## Expand the MaxQuant', sk))], ignore.case = TRUE)), '\n')
