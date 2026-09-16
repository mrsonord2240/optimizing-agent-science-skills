.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# Re-audit 2026-09-15, PTM Input 5 (Stress, regression). Anti-K-GG + global proteome. The SKILL.md MSstatsPTM block with
# the substitutions a diGly run requires (file names, mod pattern, probability column, K site suffix); everything else
# unchanged. Then the Skill's C-terminal GG-K regex (applied in R form) and the model-based FLR.
source('F:/OpenScience/audits/bio-proteomics-ptm-analysis/rerun/skillblock.R')
setwd('F:/OpenScience/audits/bio-proteomics-ptm-analysis/data/glygly')
ev0 <- read.table('evidence_glygly.txt', sep = '\t', header = TRUE, quote = '')
pcol <- grep('Probabilities', names(ev0), value = TRUE); cat('probability column:', pcol, '\n')
blk <- ptm_block()
subs <- list(c('uniprot_human.fasta', 'synthetic.fasta'), c('evidence_phospho.txt', 'evidence_glygly.txt'),
             c('Phospho..STY..Probabilities', pcol), c("'Phospho \\\\(STY\\\\)'", "'GlyGly \\\\(K\\\\)'"),
             c("'\\\\(Phospho \\\\(STY\\\\)\\\\)'", "'\\\\(GlyGly \\\\(K\\\\)\\\\)'"), c("'_[STY][0-9]+'", "'_K[0-9]+'"))
for (s in subs) { n <- lengths(regmatches(blk, gregexpr(s[1], blk, fixed = TRUE))); cat('substitute', s[1], '->', s[2], ':', n, 'x\n'); blk <- gsub(s[1], s[2], blk, fixed = TRUE) }
eval(parse(text = blk), envir = globalenv())
cat('names(input):', names(input), '| Label:', unique(adjusted$Label), '| ADJUSTED K-site rows:', nrow(adjusted), '| regulated (TREAT):', nrow(regulated), '\n')
tf <- 'truth_sites.csv'
truth_table(result$PTM.Model[grepl('_K[0-9]+', result$PTM.Model$Protein), ], tf, 'PTM.Model')
truth_table(adjusted, tf, 'ADJUSTED.Model')
ct <- ev0[grepl('K\\(GlyGly \\(K\\)\\)_$', ev0$Modified.sequence), ]
cat('C-terminal GG-K rows (Skill regex):', nrow(ct), '| distinct peptides:', length(unique(ct$Modified.sequence)), '\n')
print(unique(ct$Modified.sequence))
truth <- read.csv(tf)
art <- truth$site[truth$class == grep('artifact|cterm', unique(truth$class), value = TRUE)[1]]
cat('artifact sites in truth:', length(art), '| called in ADJUSTED:', sum(art %in% adjusted$Protein[adjusted$adj.pvalue < 0.05]), '\n')
