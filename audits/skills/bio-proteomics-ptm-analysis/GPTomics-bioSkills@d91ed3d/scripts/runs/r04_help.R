.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
db <- tools::Rd_db('MSstatsPTM')
for (f in c('groupComparisonPTM.Rd', 'MaxQtoMSstatsPTMFormat.Rd', 'dataSummarizationPTM.Rd')) {
  cat('\n==================', f, '==================\n')
  tools::Rd2txt(db[[f]], options = list(underline_titles = FALSE))
}
