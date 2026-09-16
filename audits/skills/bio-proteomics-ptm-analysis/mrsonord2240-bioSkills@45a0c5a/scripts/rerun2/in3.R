
# RE-AUDIT B, PTM Input 3 (Edge, regression of the pass-2 P2 fix): no global proteome.
# Decision-tree row route. The SKILL.md block with the global-run arguments removed, run twice:
# once with the block's own default use_unmod <- FALSE, once with use_unmod <- TRUE (the proxy the
# decision tree now offers), which crashed before pass 2.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
source('F:/OpenScience/audits/bio-proteomics-ptm-analysis/rerun/skillblock.R')
setwd('F:/OpenScience/audits/bio-proteomics-ptm-analysis/rerun2/work3')
blk <- gsub('uniprot_human.fasta', 'synthetic.fasta', ptm_block(), fixed = TRUE)
lines <- strsplit(blk, '\n')[[1]]
upto <- grep('^result <- groupComparisonPTM', lines)
noglobal <- lines[1:upto]
noglobal <- noglobal[!grepl('evidence_prot|proteinGroups = |annotation_protein', noglobal)]
cat('block carries a use_unmod flag line:', any(grepl('^use_unmod <- FALSE', noglobal)),
    '| and passes it:', any(grepl('use_unmod_peptides = use_unmod', noglobal)), '\n')

# 1) the Skill's own guard must stop when there is no protein dataset
g <- tryCatch({ eval(parse(text = paste(noglobal, collapse = '\n')), envir = globalenv()); 'NO STOP' },
              error = function(e) conditionMessage(e))
cat('with stopifnot kept:', g, '\n')

run <- function(unmod) {
  l <- noglobal[!grepl('^stopifnot', noglobal)]
  l <- sub('^use_unmod <- FALSE', paste0('use_unmod <- ', unmod), l)
  r <- tryCatch({ eval(parse(text = paste(l, collapse = '\n')), envir = globalenv())
                  get('result', envir = globalenv()) },
                error = function(e) { cat('ERROR:', conditionMessage(e), '\n'); NULL })
  cat('\nuse_unmod =', unmod, '| names(input):', if (exists('input', globalenv())) names(get('input', globalenv())) else 'n/a',
      '| names(result):', if (is.null(r)) 'ERROR' else names(r), '\n')
  if (!is.null(r)) cat('  evidence rows kept by the filter:', nrow(get('ev', globalenv())),
                       '| PTM rows:', nrow(get('input', globalenv())$PTM),
                       '| ADJUSTED.Model NULL:', is.null(r$ADJUSTED.Model), '\n')
  r
}
r0 <- run('FALSE')
if (!is.null(r0)) truth_table(r0$PTM.Model[grepl('_[STY][0-9]+', r0$PTM.Model$Protein), ],
                              'truth_sites.csv', 'phospho-only PTM.Model (UNADJUSTED)')
r1 <- run('TRUE')
if (!is.null(r1) && !is.null(r1$ADJUSTED.Model))
  truth_table(r1$ADJUSTED.Model[grepl('_[STY][0-9]+', r1$ADJUSTED.Model$Protein), ],
              'truth_sites.csv', 'use_unmod = TRUE ADJUSTED (proxy-adjusted)')
