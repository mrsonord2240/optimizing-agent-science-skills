.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# Re-audit 2026-09-15, Input 4 confirmation: the NaN z-scores come from a site with log2FC = -Inf (FC = 2^-Inf = 0,
# which passes the Skill's is.finite(FC) filter). Re-run the SKILL.md block with ONE extra filter (FC > 0) to confirm,
# and check kinase direction against SYNTHETIC truth.
SP <- 'C:/Users/User/AppData/Local/Temp/claude/f--openscience-specialist-marketplace/5c5e1ac7-a797-41ee-9a87-111d2ea0f6a7/scratchpad/ksea/KSEAapp'
source('F:/OpenScience/audits/bio-proteomics-ptm-analysis/rerun/skillblock.R')
source(file.path(SP, 'R', 'KSEA.Scores.R'))
rd <- function(f) read.table(f, sep = '\t', header = TRUE, quote = '')
adjusted <- readRDS('F:/OpenScience/audits/bio-proteomics-ptm-analysis/rerun/in1_result.rds')$adjusted
setwd('F:/OpenScience/audits/bio-proteomics-ptm-analysis/rerun/in4_ksea')
blk <- sub('library(KSEAapp)', '# library(KSEAapp)', ksea_block(), fixed = TRUE)
blk <- sub('PX <- PX[!is.na(PX$Gene) & is.finite(PX$FC), ]', 'PX <- PX[!is.na(PX$Gene) & is.finite(PX$FC) & PX$FC > 0, ]', blk, fixed = TRUE)
cat('filter line patched:', grepl('PX$FC > 0', blk, fixed = TRUE), '\n')
eval(parse(text = blk), envir = globalenv())
print(kinase_scores[order(kinase_scores$z.score), c('Kinase.Gene', 'm', 'z.score', 'FDR')])
truth <- read.csv('F:/OpenScience/audits/bio-proteomics-ptm-analysis/data/phospho/truth_sites.csv')
syn <- read.delim('F:/OpenScience/audits/bio-proteomics-ptm-analysis/data/phospho/kinase_substrate_SYNTHETIC.tsv')
print(aggregate(true_occupancy_log2fc ~ KINASE, data = merge(syn, truth, by.x = 'SUB_ACC_ID', by.y = 'protein'), FUN = mean))
