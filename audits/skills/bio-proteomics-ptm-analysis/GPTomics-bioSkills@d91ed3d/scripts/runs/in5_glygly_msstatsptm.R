.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# Input 5 (Stress), part 2: MSstatsPTM on the SYNTHETIC diGly evidence + paired global proteome.
# Skill block with mod_id switched to GlyGly and the three fixes Input 1 needed (evidence_prot, append = FALSE,
# data.type = 'LabelFree').
setwd('F:/OpenScience/audits/bio-proteomics-ptm-analysis/data/glygly')
suppressPackageStartupMessages({library(MSstatsPTM); library(data.table)})
rd <- function(f) read.table(f, sep = '\t', header = TRUE, quote = '')
input <- MaxQtoMSstatsPTMFormat(
  evidence = rd('evidence_glygly.txt'), annotation = read.csv('annotation_ptm.csv'),
  fasta_path = 'synthetic.fasta', fasta_protein_name = 'uniprot_ac',
  evidence_prot = rd('evidence_global.txt'), proteinGroups = rd('proteinGroups_global.txt'),
  annotation_protein = read.csv('annotation_protein.csv'),
  mod_id = '\\(GlyGly \\(K\\)\\)', which_proteinid_ptm = 'Proteins', which_proteinid_protein = 'Proteins',
  use_unmod_peptides = FALSE, use_log_file = FALSE, verbose = FALSE)
cat('names(input):', paste(names(input), collapse = ', '), '| PTM rows', nrow(input$PTM), '\n')
cat('PTM site labels (first 4):', paste(head(unique(input$PTM$ProteinName), 4), collapse = ' | '), '\n')
s <- dataSummarizationPTM(input, use_log_file = FALSE, append = FALSE, verbose = FALSE)
r <- groupComparisonPTM(s, data.type = 'LabelFree', use_log_file = FALSE, verbose = FALSE)
adjusted <- r$ADJUSTED.Model
regulated <- adjusted[!is.na(adjusted$adj.pvalue) & adjusted$adj.pvalue < 0.05 & abs(adjusted$log2FC) > 1, ]
truth <- fread('truth_sites.csv')
pm <- as.data.table(r$PTM.Model)[, .(site = as.character(Protein), fc_ptm = log2FC, p_ptm = adj.pvalue)]
am <- as.data.table(adjusted)[, .(site = as.character(Protein), fc_adj = log2FC, p_adj = adj.pvalue)]
m <- merge(merge(truth, pm, by = 'site', all.x = TRUE), am, by = 'site', all.x = TRUE)
m[, `:=`(call_ptm = !is.na(p_ptm) & p_ptm < 0.05 & abs(fc_ptm) > 1, call_adj = !is.na(p_adj) & p_adj < 0.05 & abs(fc_adj) > 1)]
print(m[, .(n = .N, tested = sum(!is.na(p_adj)), called_PTM.Model = sum(call_ptm), called_ADJUSTED = sum(call_adj)), by = class])
cat('Skill-filter regulated rows:', nrow(regulated), '\n')
