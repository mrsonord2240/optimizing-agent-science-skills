
# Input E part 2: run the SKILL.md MSstatsPTM block VERBATIM after only swapping in a TMT11 annotation,
# which is the one thing a TMT user changes first. Does the Skill's route reach a result, or does it need
# a different converter, summarizer and data.type that the Skill never mentions?
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
source('F:/OpenScience/audits/bio-proteomics-ptm-analysis/rerun/skillblock.R')
setwd('F:/OpenScience/audits/bio-proteomics-ptm-analysis/rerun2/workE')
blk <- gsub('uniprot_human.fasta', 'synthetic.fasta', ptm_block(), fixed = TRUE)
blk <- gsub("annotation_ptm.csv", "annotation_ptm_tmt.csv", blk, fixed = TRUE)
r <- tryCatch({ eval(parse(text = blk), envir = globalenv()); 'COMPLETED' },
              error = function(e) paste('ERROR:', conditionMessage(e)))
cat('\nSKILL.md block with a TMT11 annotation:', r, '\n')
cat('block text contains labeling_type:', grepl('labeling_type', blk),
    '| TMT_keyword:', grepl('TMT_keyword', blk),
    '| dataSummarizationPTM_TMT:', grepl('dataSummarizationPTM_TMT', blk),
    "| data.type = 'TMT':", grepl("data.type = 'TMT'", blk), '\n')
