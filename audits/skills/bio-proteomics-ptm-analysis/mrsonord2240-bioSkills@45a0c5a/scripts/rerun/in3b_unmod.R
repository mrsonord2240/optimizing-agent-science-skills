.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# Re-audit 2026-09-15, Input 3 follow-up: does the Skill's evidence pre-filter (modified rows only) defeat the
# decision tree's use_unmod_peptides = TRUE proxy? (i) Skill-filtered evidence, (ii) class-I rule on modified rows only.
# Also (c): which null / protein-driven sites does Input 1 call, and are the nulls multiplicity-switch proteins?
suppressPackageStartupMessages(library(MSstatsPTM))
source('F:/OpenScience/audits/bio-proteomics-ptm-analysis/rerun/skillblock.R')
setwd('F:/OpenScience/audits/bio-proteomics-ptm-analysis/data/phospho')
rd <- function(f) read.table(f, sep = '\t', header = TRUE, quote = '')
ev0 <- rd('evidence_phospho.txt')
sp <- vapply(regmatches(ev0$Phospho..STY..Probabilities, gregexpr('(?<=\\()[0-9.]+(?=\\))', ev0$Phospho..STY..Probabilities, perl = TRUE)),
             function(p) if (length(p)) max(as.numeric(p)) else NA_real_, numeric(1))
mod <- grepl('Phospho \\(STY\\)', ev0$Modified.sequence)
ev_skill <- ev0[mod & !is.na(sp) & sp >= 0.75, ]
ev_keep_unmod <- ev0[(!mod) | (!is.na(sp) & sp >= 0.75), ]
cat('evidence rows:', nrow(ev0), '| unmodified:', sum(!mod), '| unmodified left after Skill filter:', sum(!grepl('Phospho', ev_skill$Modified.sequence)), '\n')
go <- function(ev, label) {
  r <- tryCatch({
    input <- MaxQtoMSstatsPTMFormat(evidence = ev, annotation = read.csv('annotation_ptm.csv'), fasta_path = 'synthetic.fasta',
                                    mod_id = '\\(Phospho \\(STY\\)\\)', which_proteinid_ptm = 'Proteins', use_unmod_peptides = TRUE)
    s <- dataSummarizationPTM(input, use_log_file = FALSE, append = FALSE)
    contrast <- matrix(c(-1, 1), nrow = 1, dimnames = list('Treatment vs Control', c('Control', 'Treatment')))
    res <- groupComparisonPTM(s, data.type = 'LabelFree', contrast.matrix = contrast)
    cat(label, ': names(input)', names(input), '| names(result)', names(res), '\n')
    if (!is.null(res$ADJUSTED.Model)) truth_table(res$ADJUSTED.Model[grepl('_[STY][0-9]+', res$ADJUSTED.Model$Protein), ], 'truth_sites.csv', paste(label, 'proxy-adjusted'))
    'ok'
  }, error = function(e) paste('ERROR:', conditionMessage(e)))
  cat(label, '->', r, '\n')
}
go(ev_skill, '(i) Skill-filtered evidence')
go(ev_keep_unmod, '(ii) unmodified rows kept')
x <- readRDS('F:/OpenScience/audits/bio-proteomics-ptm-analysis/rerun/in1_result.rds'); adj <- x$adjusted
truth <- read.csv('truth_sites.csv')
m <- merge(adj[, c('Protein', 'log2FC', 'adj.pvalue', 'adj.pvalue_lfc')], truth, by.x = 'Protein', by.y = 'site')
print(m[m$class %in% c('null', 'protein_driven') & m$adj.pvalue < 0.05, c('Protein', 'class', 'multiplicity_switch', 'log2FC', 'adj.pvalue', 'adj.pvalue_lfc', 'true_protein_log2fc')])
cat('ADJUSTED rows with infinite log2FC:', sum(!is.finite(adj$log2FC)), '\n'); print(adj[!is.finite(adj$log2FC), c('Protein', 'log2FC', 'adj.pvalue')])
