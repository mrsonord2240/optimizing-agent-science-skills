.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# Input 1 (Canonical), step B: the two minimal adaptations the verbatim run needed
#   (1) evidence_prot = global evidence (without it MaxQtoMSstatsPTMFormat returns no $PROTEIN)
#   (2) dataSummarizationPTM(..., append = FALSE) (use_log_file = FALSE alone trips an assertion)
#   (3) groupComparisonPTM(data.type = 'LabelFree') ('LF' matches neither branch -> "object 'ptm_model' not found")
# then compare PTM.Model vs ADJUSTED.Model against the SYNTHETIC truth.
setwd('F:/OpenScience/audits/bio-proteomics-ptm-analysis/data/phospho')
suppressPackageStartupMessages({library(MSstatsPTM); library(data.table)})

rd <- function(f) read.table(f, sep = '\t', header = TRUE, quote = '')
input <- MaxQtoMSstatsPTMFormat(
  evidence = rd('evidence_phospho.txt'),
  annotation = read.csv('annotation_ptm.csv'),
  fasta_path = 'synthetic.fasta',
  fasta_protein_name = 'uniprot_ac',
  evidence_prot = rd('evidence_global.txt'),            # <- added
  proteinGroups = rd('proteinGroups_global.txt'),
  annotation_protein = read.csv('annotation_protein.csv'),
  mod_id = '\\(Phospho \\(STY\\)\\)',
  which_proteinid_ptm = 'Proteins',
  which_proteinid_protein = 'Proteins',
  use_unmod_peptides = FALSE,
  use_log_file = FALSE, verbose = FALSE
)
cat('names(input):', paste(names(input), collapse = ', '), '| PTM rows', nrow(input$PTM), '| PROTEIN rows', nrow(input$PROTEIN), '\n')
cat('example PTM ProteinName values:', paste(head(unique(input$PTM$ProteinName), 4), collapse = ' | '), '\n')

summarized <- dataSummarizationPTM(input, use_log_file = FALSE, append = FALSE, verbose = FALSE)
result <- groupComparisonPTM(summarized, data.type = 'LabelFree', use_log_file = FALSE, verbose = FALSE)
cat('names(result):', paste(names(result), collapse = ', '), '\n')
adjusted <- result$ADJUSTED.Model
cat('ADJUSTED.Model columns:', paste(colnames(adjusted), collapse = ', '), '\n')
cat('Label (contrast) values:', paste(unique(adjusted$Label), collapse = ', '), '\n')

# The Skill's regulated filter, verbatim
regulated <- adjusted[!is.na(adjusted$adj.pvalue) & adjusted$adj.pvalue < 0.05 & abs(adjusted$log2FC) > 1, ]

truth <- fread('truth_sites.csv')
ptm <- as.data.table(result$PTM.Model); adj <- as.data.table(adjusted)
key <- function(x) sub('^(P[0-9]{5})_([STY])([0-9]+)$', '\\1_\\2\\3', x)
ptm[, site := key(as.character(Protein))]; adj[, site := key(as.character(Protein))]
m <- merge(truth, ptm[, .(site, fc_ptm = log2FC, p_ptm = adj.pvalue)], by = 'site', all.x = TRUE)
m <- merge(m, adj[, .(site, fc_adj = log2FC, p_adj = adj.pvalue)], by = 'site', all.x = TRUE)
m[, call_ptm := !is.na(p_ptm) & p_ptm < 0.05 & abs(fc_ptm) > 1]
m[, call_adj := !is.na(p_adj) & p_adj < 0.05 & abs(fc_adj) > 1]
m[, call_adj_sig := !is.na(p_adj) & p_adj < 0.05]
cat('\nPer truth class (n sites tested of n truth sites; calls under the Skill filter):\n')
print(m[, .(n = .N, tested_ptm = sum(!is.na(p_ptm)), tested_adj = sum(!is.na(p_adj)),
            called_PTM.Model = sum(call_ptm), called_ADJUSTED = sum(call_adj), adj_sig_any_FC = sum(call_adj_sig),
            mean_fc_ptm = round(mean(fc_ptm, na.rm = TRUE), 2), mean_fc_adj = round(mean(abs(fc_adj), na.rm = TRUE), 2)),
        by = class])
cat('\nSites in ADJUSTED.Model whose truth loc_prob < 0.75 (class II/III, no localization filter in this path):\n')
print(m[!is.na(p_adj) & loc_prob < 0.75, .(site, class, loc_prob, fc_adj = round(fc_adj, 2), p_adj = signif(p_adj, 2))])
cat('\nMasked sites (observed ~0, true occupancy -1.2):\n')
print(m[class == 'masked', .(site, fc_ptm = round(fc_ptm, 2), p_ptm = signif(p_ptm, 2), fc_adj = round(fc_adj, 2), p_adj = signif(p_adj, 2))])
cat('\nProtein-driven sites:\n')
print(m[class == 'protein_driven', .(site, fc_ptm = round(fc_ptm, 2), p_ptm = signif(p_ptm, 2), fc_adj = round(fc_adj, 2), p_adj = signif(p_adj, 2))])
cat('\nnrow(regulated) under the Skill filter:', nrow(regulated), '\n')
cat('regulated sites:', paste(sort(key(as.character(regulated$Protein))), collapse = ', '), '\n')
saveRDS(list(result = result, merged = m), 'F:/OpenScience/audits/bio-proteomics-ptm-analysis/runs/in1_result.rds')
fwrite(adj, 'F:/OpenScience/audits/bio-proteomics-ptm-analysis/runs/in1_adjusted_model.csv')
fwrite(ptm, 'F:/OpenScience/audits/bio-proteomics-ptm-analysis/runs/in1_ptm_model.csv')
