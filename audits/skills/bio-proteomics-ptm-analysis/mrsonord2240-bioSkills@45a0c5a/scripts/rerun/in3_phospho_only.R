.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# Re-audit 2026-09-15, PTM Input 3 (Edge, regression). No global proteome. Following the decision-tree row: the SKILL.md
# block with the global-run arguments and the stopifnot removed (the Skill's own guard fires first, as a check), then
# PTM.Model reported as UNADJUSTED; optional use_unmod_peptides = TRUE labelled proxy-adjusted.
source('F:/OpenScience/audits/bio-proteomics-ptm-analysis/rerun/skillblock.R')
setwd('F:/OpenScience/audits/bio-proteomics-ptm-analysis/data/phospho')
blk <- gsub('uniprot_human.fasta', 'synthetic.fasta', ptm_block(), fixed = TRUE)
lines <- strsplit(blk, '\n')[[1]]
upto <- grep('^result <- groupComparisonPTM', lines)
noglobal <- lines[1:upto]
noglobal <- noglobal[!grepl('evidence_prot|proteinGroups = |annotation_protein', noglobal)]
# 1) Skill guard left in: must stop
g <- tryCatch({eval(parse(text = paste(noglobal, collapse = '\n')), envir = globalenv()); 'no stop'}, error = function(e) conditionMessage(e))
cat('with stopifnot kept:', g, '\n')
run <- function(unmod) {
  l <- noglobal[!grepl('^stopifnot', noglobal)]
  l <- sub('use_unmod_peptides = FALSE', paste0('use_unmod_peptides = ', unmod), l, fixed = TRUE)
  eval(parse(text = paste(l, collapse = '\n')), envir = globalenv())
  cat('\nuse_unmod_peptides =', unmod, '| names(input):', names(input), '| names(result):', names(result), '\n')
  get('result', envir = globalenv())
}
r0 <- run('FALSE')
cat('ADJUSTED.Model is NULL:', is.null(r0$ADJUSTED.Model), '\n')
truth_table(r0$PTM.Model[grepl('_[STY][0-9]+', r0$PTM.Model$Protein), ], 'truth_sites.csv', 'phospho-only PTM.Model (UNADJUSTED)')
r1 <- run('TRUE')
if (!is.null(r1$ADJUSTED.Model)) truth_table(r1$ADJUSTED.Model[grepl('_[STY][0-9]+', r1$ADJUSTED.Model$Protein), ], 'truth_sites.csv', 'use_unmod_peptides=TRUE ADJUSTED (proxy-adjusted)')
