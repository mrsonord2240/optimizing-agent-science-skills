# Pass-5 confirmation audit, Input 8: the NEW "TMT / isobaric plexes" block of the fixed SKILL.md,
# extracted programmatically from the fork and eval'd VERBATIM (only file names substituted), on a
# SYNTHETIC TMT10 evidence pair built by pass5/make_tmt.py from this audit's own labelled set, so
# data/phospho/truth_sites.csv still applies.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({library(MSstatsPTM); library(MSstatsTMT)})
cat('MSstatsPTM', as.character(packageVersion('MSstatsPTM')),
    '| MSstatsTMT', as.character(packageVersion('MSstatsTMT')),
    '| KSEAapp', as.character(packageVersion('KSEAapp')), '\n')

source('F:/OpenScience/audits/bio-proteomics-ptm-analysis/rerun/skillblock.R')
blocks <- skill_r_blocks()
tmt <- blocks[grepl('dataSummarizationPTM_TMT', blocks)][1]
stopifnot(!is.na(tmt))
cat('TMT block found:', nchar(tmt), 'chars | labeling_type:', grepl("labeling_type = 'TMT'", tmt),
    '| data.type TMT:', grepl("data.type = 'TMT'", tmt), '\n')

setwd('F:/OpenScience/audits/bio-proteomics-ptm-analysis/pass5/tmt')
blk <- gsub('uniprot_human.fasta', 'synthetic.fasta', tmt, fixed = TRUE)

cat('\n=== (a) channel naming: does the SKILL.md claim "channel.1 ... channel.N" hold? ===\n')
# The evidence carries MaxQuant's 0-indexed "Reporter intensity corrected 0..9".
for (ann in c('annotation_ptm_tmt_ch1.csv', 'annotation_ptm_tmt.csv')) {
  b <- gsub('annotation_ptm_tmt.csv', ann, blk, fixed = TRUE)
  b <- gsub('annotation_protein_tmt.csv',
            sub('ptm', 'protein', ann, fixed = TRUE), b, fixed = TRUE)
  r <- tryCatch({ eval(parse(text = b), envir = new.env(parent = globalenv())); 'COMPLETED' },
                error = function(e) paste('ERROR:', conditionMessage(e)))
  cat('  ', ann, '->', substr(r, 1, 220), '\n')
}

cat('\n=== (b) the block, run verbatim with the annotation that works ===\n')
env <- new.env(parent = globalenv())
ok <- tryCatch({ eval(parse(text = blk), envir = env); 'COMPLETED' },
               error = function(e) paste('ERROR:', conditionMessage(e)))
cat('status:', ok, '\n')
if (ok == 'COMPLETED') {
  input <- get('input', env); result <- get('result', env); adjusted <- get('adjusted', env)
  cat('names(input):', paste(names(input), collapse = ' '), '\n')
  cat('models returned:', paste(names(result), collapse = ' '), '\n')
  cat('ADJUSTED site rows:', nrow(adjusted), '| Label(s):',
      paste(unique(adjusted$Label), collapse = ','), '\n')

  ptm <- result$PTM.Model
  ptm <- ptm[grepl('_[STY][0-9]+', ptm$Protein), ]
  truth <- read.csv('truth_sites.csv')
  norm_id <- function(x) sub('^([A-Z0-9]+)_([STY][0-9]+)$', '\\1_\\2', x)
  call_set <- function(df) df$Protein[!is.na(df$adj.pvalue) & df$adj.pvalue < 0.05]
  cat('\n-- protein adjustment against planted truth --\n')
  for (cl in c('protein_driven', 'site_regulated', 'masked', 'null')) {
    s <- truth$site[truth$class == cl]
    cat(sprintf('%-15s n=%2d | tested PTM %2d ADJ %2d | called PTM %d/%d -> ADJ %d/%d\n',
        cl, length(s), sum(s %in% ptm$Protein), sum(s %in% adjusted$Protein),
        sum(s %in% call_set(ptm)), length(s), sum(s %in% call_set(adjusted)), length(s)))
  }
  m <- merge(adjusted[, c('Protein', 'log2FC')], truth, by.x = 'Protein', by.y = 'site')
  m <- m[is.finite(m$log2FC), ]
  reg <- m[m$class %in% c('site_regulated', 'masked'), ]
  cat('\nsign agreement (adjusted log2FC vs true occupancy log2FC) on regulated+masked: ',
      sum(sign(reg$log2FC) == sign(reg$true_occupancy_log2fc)), '/', nrow(reg), '\n', sep = '')
  cat('Spearman rho adjusted log2FC vs true occupancy log2FC: ',
      round(cor(m$log2FC, m$true_occupancy_log2fc, method = 'spearman'), 3), '\n', sep = '')
}
