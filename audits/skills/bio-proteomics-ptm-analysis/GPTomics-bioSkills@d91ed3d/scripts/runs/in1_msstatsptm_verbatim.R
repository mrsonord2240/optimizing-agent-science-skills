.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# Input 1 (Canonical), step A: SKILL.md lines 140-172 VERBATIM; only file names mapped to the SYNTHETIC data.
setwd('F:/OpenScience/audits/bio-proteomics-ptm-analysis/data/phospho')
suppressPackageStartupMessages(library(MSstatsPTM))
cat('MSstatsPTM', as.character(packageVersion('MSstatsPTM')), '\n')

input <- MaxQtoMSstatsPTMFormat(
  evidence = read.table('evidence_phospho.txt', sep = '\t', header = TRUE, quote = ''),
  annotation = read.csv('annotation_ptm.csv'),
  fasta_path = 'synthetic.fasta',
  fasta_protein_name = 'uniprot_ac',
  proteinGroups = read.table('proteinGroups_global.txt', sep = '\t', header = TRUE, quote = ''),
  annotation_protein = read.csv('annotation_protein.csv'),
  mod_id = '\\(Phospho \\(STY\\)\\)',
  which_proteinid_ptm = 'Proteins',
  use_unmod_peptides = FALSE
)
cat('\nnames(input):', paste(names(input), collapse = ', '), '\n')
cat('PTM rows:', nrow(input$PTM), '| PROTEIN is NULL:', is.null(input$PROTEIN), '\n')

summarized <- tryCatch(dataSummarizationPTM(input, use_log_file = FALSE),
                       error = function(e) { cat('dataSummarizationPTM ERROR:', conditionMessage(e), '\n'); NULL })
if (!is.null(summarized)) {
  cat('names(summarized):', paste(names(summarized), collapse = ', '), '\n')
  result <- tryCatch(groupComparisonPTM(summarized, data.type = 'LF'),
                     error = function(e) { cat('groupComparisonPTM ERROR:', conditionMessage(e), '\n'); NULL })
  if (!is.null(result)) {
    cat('names(result):', paste(names(result), collapse = ', '), '\n')
    adjusted <- result$ADJUSTED.Model
    cat('is.null(result$ADJUSTED.Model):', is.null(adjusted), '\n')
    regulated <- tryCatch(adjusted[!is.na(adjusted$adj.pvalue) & adjusted$adj.pvalue < 0.05 & abs(adjusted$log2FC) > 1, ],
                          error = function(e) { cat('regulated-filter ERROR:', conditionMessage(e), '\n'); 'ERR' })
    cat('class(regulated):', class(regulated), '| NROW:', NROW(regulated), '\n')
    cat('PTM.Model rows:', NROW(result$PTM.Model), '\n')
  }
}
