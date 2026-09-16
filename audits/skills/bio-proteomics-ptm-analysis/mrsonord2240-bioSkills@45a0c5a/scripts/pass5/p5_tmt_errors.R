# Verify the two NEW TMT Common Errors rows reproduce their exact messages.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({library(MSstatsPTM); library(MSstatsTMT)})
source('F:/OpenScience/audits/bio-proteomics-ptm-analysis/rerun/skillblock.R')
setwd('F:/OpenScience/audits/bio-proteomics-ptm-analysis/pass5/tmt')
tmt <- skill_r_blocks()[grepl('dataSummarizationPTM_TMT', skill_r_blocks())][1]
blk <- gsub('uniprot_human.fasta', 'synthetic.fasta', tmt, fixed = TRUE)

cat('--- row 1: label-free ANNOTATION passed with labeling_type = TMT ---\n')
b <- gsub("annotation_ptm_tmt.csv", "../work1/annotation_ptm.csv", blk, fixed = TRUE)
b <- gsub("annotation_protein_tmt.csv", "../work1/annotation_protein.csv", b, fixed = TRUE)
r <- tryCatch({eval(parse(text=b), envir=new.env(parent=globalenv())); 'COMPLETED'},
              error=function(e) conditionMessage(e))
cat('  ', substr(gsub('[[:space:]]+',' ',r),1,300), '\n')

cat('--- row 2: TMT evidence left on the default labeling_type = LF ---\n')
b2 <- gsub("  labeling_type = 'TMT',          # the single converter switch; default is 'LF'\n", '', blk, fixed = TRUE)
b2 <- gsub("dataSummarizationPTM_TMT", "dataSummarizationPTM", b2, fixed = TRUE)
cat('  labeling_type removed:', !grepl('labeling_type', b2), '\n')
r2 <- tryCatch({eval(parse(text=b2), envir=new.env(parent=globalenv())); 'COMPLETED'},
               error=function(e) conditionMessage(e))
cat('  ', substr(gsub('[[:space:]]+',' ',r2),1,300), '\n')
