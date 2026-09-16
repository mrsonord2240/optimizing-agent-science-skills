.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({library(MSstatsPTM); library(MSstatsTMT)})
source('F:/OpenScience/audits/bio-proteomics-ptm-analysis/rerun/skillblock.R')
setwd('F:/OpenScience/audits/bio-proteomics-ptm-analysis/pass5/tmt')
tmt <- skill_r_blocks()[grepl('dataSummarizationPTM_TMT', skill_r_blocks())][1]
b <- gsub('uniprot_human.fasta', 'synthetic.fasta', tmt, fixed = TRUE)
# the true "forgot the switch": TMT EVIDENCE + an LF-shaped annotation, labeling_type left at default
b <- gsub("  labeling_type = 'TMT',          # the single converter switch; default is 'LF'\n", '', b, fixed=TRUE)
b <- gsub("dataSummarizationPTM_TMT", "dataSummarizationPTM", b, fixed=TRUE)
b <- gsub("annotation_ptm_tmt.csv", "annotation_lf_ptm.csv", b, fixed=TRUE)
b <- gsub("annotation_protein_tmt.csv", "annotation_lf_protein.csv", b, fixed=TRUE)
write.csv(data.frame(Raw.file='plex1', Condition=c('Control','Treatment'),
                     BioReplicate=c('S1','S2'), IsotopeLabelType='L'), 'annotation_lf_ptm.csv', row.names=FALSE)
file.copy('annotation_lf_ptm.csv','annotation_lf_protein.csv', overwrite=TRUE)
r <- tryCatch({eval(parse(text=b), envir=new.env(parent=globalenv())); 'COMPLETED'},
              error=function(e) conditionMessage(e))
cat('TMT evidence + LF annotation, labeling_type default:\n  ',
    substr(gsub('[[:space:]]+',' ',r),1,300), '\n')
