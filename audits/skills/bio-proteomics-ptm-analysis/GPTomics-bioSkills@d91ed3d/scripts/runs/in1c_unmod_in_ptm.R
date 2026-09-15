.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# Input 1 addendum: with use_unmod_peptides = FALSE (Skill setting) the unmodified peptides that co-enrich in the
# phospho runs stay in $PTM and are tested as if they were sites. Compare with evidence pre-filtered to Phospho rows.
setwd('F:/OpenScience/audits/bio-proteomics-ptm-analysis/data/phospho')
suppressPackageStartupMessages({library(MSstatsPTM); library(data.table)})
rd <- function(f) read.table(f, sep = '\t', header = TRUE, quote = '')
ev <- rd('evidence_phospho.txt')
cat('enriched evidence rows:', nrow(ev), '| unmodified rows:', sum(ev$Modifications == 'Unmodified'), '\n')
go <- function(evd, tag) {
  inp <- MaxQtoMSstatsPTMFormat(evidence = evd, annotation = read.csv('annotation_ptm.csv'), fasta_path = 'synthetic.fasta',
                                evidence_prot = rd('evidence_global.txt'), proteinGroups = rd('proteinGroups_global.txt'),
                                annotation_protein = read.csv('annotation_protein.csv'), mod_id = '\\(Phospho \\(STY\\)\\)',
                                which_proteinid_ptm = 'Proteins', use_unmod_peptides = FALSE, use_log_file = FALSE, verbose = FALSE)
  s <- dataSummarizationPTM(inp, use_log_file = FALSE, append = FALSE, verbose = FALSE)
  r <- groupComparisonPTM(s, data.type = 'LabelFree', use_log_file = FALSE, verbose = FALSE)
  a <- as.data.table(r$ADJUSTED.Model)
  reg <- a[!is.na(adj.pvalue) & adj.pvalue < 0.05 & abs(log2FC) > 1]
  cat(sprintf('%-38s ADJUSTED rows %3d | rows without a site suffix %3d | regulated %2d | adj.p sig any FC %2d\n', tag,
              nrow(a), sum(!grepl('_', a$Protein)), nrow(reg), sum(a$adj.pvalue < 0.05, na.rm = TRUE)))
  a
}
a1 <- go(ev, 'as written (unmodified rows kept)')
a2 <- go(ev[grepl('Phospho', ev$Modified.sequence), ], 'evidence pre-filtered to Phospho rows')
x <- merge(a1[grepl('_', Protein), .(Protein, p_kept = adj.pvalue)], a2[, .(Protein, p_filt = adj.pvalue)], by = 'Protein')
cat('median ratio adj.p(kept) / adj.p(filtered) over site rows:', round(median(x$p_kept / x$p_filt, na.rm = TRUE), 2), '\n')
