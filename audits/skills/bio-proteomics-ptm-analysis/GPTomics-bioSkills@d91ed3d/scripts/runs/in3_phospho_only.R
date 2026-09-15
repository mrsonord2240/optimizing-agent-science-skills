.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# Input 3 (Edge): phospho-enriched runs only, no global proteome (SYNTHETIC data).
# Skill route: Decision Tree row 'No global proteome available' -> report UNADJUSTED + flag the confound.
setwd('F:/OpenScience/audits/bio-proteomics-ptm-analysis/data/phospho')
suppressPackageStartupMessages({library(MSstatsPTM); library(data.table)})
rd <- function(f) read.table(f, sep = '\t', header = TRUE, quote = '')
ev <- rd('evidence_phospho.txt'); ann <- read.csv('annotation_ptm.csv')
truth <- fread('truth_sites.csv')

run <- function(use_unmod, tag) {
  cat('\n==========', tag, '==========\n')
  inp <- MaxQtoMSstatsPTMFormat(evidence = ev, annotation = ann, fasta_path = 'synthetic.fasta',
                                mod_id = '\\(Phospho \\(STY\\)\\)', which_proteinid_ptm = 'Proteins',
                                use_unmod_peptides = use_unmod, use_log_file = FALSE, verbose = FALSE)
  cat('names(input):', paste(names(inp), collapse = ', '), '| PROTEIN rows:', NROW(inp$PROTEIN), '\n')
  s <- dataSummarizationPTM(inp, use_log_file = FALSE, append = FALSE, verbose = FALSE)
  r <- groupComparisonPTM(s, data.type = 'LabelFree', use_log_file = FALSE, verbose = FALSE)
  cat('names(result):', paste(names(r), collapse = ', '), '\n')
  # the Skill's post-processing, verbatim
  adjusted <- r$ADJUSTED.Model
  regulated <- tryCatch(adjusted[!is.na(adjusted$adj.pvalue) & adjusted$adj.pvalue < 0.05 & abs(adjusted$log2FC) > 1, ],
                        error = function(e) paste('ERROR:', conditionMessage(e)))
  cat('Skill filter on result$ADJUSTED.Model -> class:', class(regulated), '| NROW:', NROW(regulated), '\n')
  pm <- as.data.table(r$PTM.Model)
  pm[, site := as.character(Protein)]
  m <- merge(truth, pm[, .(site, fc = log2FC, p = adj.pvalue)], by = 'site')
  m[, call := !is.na(p) & p < 0.05 & abs(fc) > 1]
  cat('PTM.Model (unadjusted) calls by truth class:\n')
  print(m[, .(tested = .N, called = sum(call)), by = class])
  if (!is.null(adjusted)) {
    am <- as.data.table(adjusted); am[, site := as.character(Protein)]
    ma <- merge(truth, am[, .(site, fc = log2FC, p = adj.pvalue, Adjusted)], by = 'site')
    ma[, call := !is.na(p) & p < 0.05 & abs(fc) > 1]
    cat('ADJUSTED.Model calls by truth class (protein proxy = unmodified peptides co-enriched in the phospho runs):\n')
    print(ma[, .(tested = .N, adjusted_rows = sum(Adjusted), called = sum(call)), by = class])
  }
}
run(FALSE, 'use_unmod_peptides = FALSE (Skill setting), no evidence_prot')
run(TRUE, 'use_unmod_peptides = TRUE (MSstatsPTM option the Skill never mentions)')
