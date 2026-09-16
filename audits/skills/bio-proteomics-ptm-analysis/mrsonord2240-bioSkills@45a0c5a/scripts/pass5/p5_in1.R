
# RE-AUDIT B (2026-09-15), PTM Input 1 (Canonical, regression after pass 2 d1b8fdc).
# SKILL.md MSstatsPTM block VERBATIM from the fork, run in a fresh copy of the SYNTHETIC audit data,
# with ONE substitution: 'uniprot_human.fasta' -> the synthetic FASTA shipped with the audit data.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
source('F:/OpenScience/audits/bio-proteomics-ptm-analysis/rerun/skillblock.R')
RR <- 'F:/OpenScience/audits/bio-proteomics-ptm-analysis/pass5'
blk <- gsub('uniprot_human.fasta', 'synthetic.fasta', ptm_block(), fixed = TRUE)
setwd(file.path(RR, 'work1'))
cat('MSstatsPTM', as.character(packageVersion('MSstatsPTM')), '| use_unmod default in block:',
    grepl('use_unmod <- FALSE', blk), '\n')
eval(parse(text = blk), envir = globalenv())
cat('\nBLOCK ran. names(input):', names(input), '| names(result):', names(result), '\n')
cat('Label:', unique(result$ADJUSTED.Model$Label), '| ADJUSTED site rows:', nrow(adjusted),
    '| regulated (TREAT lfc=1, BH<0.05):', nrow(regulated), '\n')
tf <- 'truth_sites.csv'
truth_table(result$PTM.Model[grepl('_[STY][0-9]+', result$PTM.Model$Protein), ], tf, 'PTM.Model (unadjusted) adj.p<0.05')
truth_table(adjusted, tf, 'ADJUSTED.Model adj.p<0.05')
truth <- read.csv(tf)
reg <- merge(regulated[, c('Protein','log2FC','adj.pvalue_lfc')], truth, by.x='Protein', by.y='site')
cat('\nregulated by TREAT, by truth class:\n'); print(table(reg$class))
cat('sign agreement on site_regulated:',
    with(reg[reg$class=='site_regulated',], sum(sign(log2FC)==sign(true_occupancy_log2fc))), '/', sum(reg$class=='site_regulated'), '\n')
tested <- merge(data.frame(Protein=adjusted$Protein), truth, by.x='Protein', by.y='site')
cat('tested sites with truth loc_prob < 0.75:', sum(tested$loc_prob < 0.75),
    '| bare protein rows in raw ADJUSTED.Model:', sum(!grepl('_[STY][0-9]+', result$ADJUSTED.Model$Protein)), '\n')
cat('non-finite log2FC rows in ADJUSTED.Model:', sum(!is.finite(adjusted$log2FC)),
    '| of which -Inf:', sum(adjusted$log2FC == -Inf, na.rm=TRUE), '| +Inf:', sum(adjusted$log2FC == Inf, na.rm=TRUE), '\n')
dbl <- adjusted[!is.na(adjusted$adj.pvalue) & adjusted$adj.pvalue < 0.05 & abs(adjusted$log2FC) > 1, ]
cat('post-hoc double filter would call:', nrow(dbl), 'vs TREAT', nrow(regulated), '\n')
saveRDS(list(result=result, adjusted=adjusted), file.path(RR, 'in1_result.rds'))
write.csv(adjusted, file.path(RR, 'in1_adjusted.csv'), row.names = FALSE)
