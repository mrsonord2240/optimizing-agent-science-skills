.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# Re-audit 2026-09-15, PTM Input 4 (Variant B, regression): kinase activity with the SKILL.md KSEAapp block VERBATIM
# (extracted from the fork). KSEAapp is not installed in the shared venv and R installs are not allowed there, so the
# CRAN KSEAapp 2.0 source (downloaded to the scratchpad, not installed) is sourced and the block's library(KSEAapp)
# line is skipped. The prior is the SYNTHETIC kinase-substrate table rebuilt in the real PSP&NetworKIN column layout.
source('F:/OpenScience/audits/bio-proteomics-ptm-analysis/rerun/skillblock.R')
SP <- 'C:/Users/User/AppData/Local/Temp/claude/f--openscience-specialist-marketplace/5c5e1ac7-a797-41ee-9a87-111d2ea0f6a7/scratchpad/ksea/KSEAapp'
source(file.path(SP, 'R', 'KSEA.Scores.R'))
load(file.path(SP, 'data', 'KSData.RData')); load(file.path(SP, 'data', 'PX.RData'))
demoKS <- KSData; demoPX <- PX
cat('demo KSData columns:', paste(names(demoKS), collapse = ', '), '| rows', nrow(demoKS), '\n')

# 1) sign behaviour on the package demo (FC vs 1/FC)
s1 <- KSEA.Scores(demoKS, demoPX, NetworKIN = FALSE)
inv <- demoPX; inv$FC <- 1 / as.numeric(as.character(inv$FC))
s2 <- KSEA.Scores(demoKS, inv, NetworKIN = FALSE)
mm <- merge(s1[, c('Kinase.Gene', 'z.score')], s2[, c('Kinase.Gene', 'z.score')], by = 'Kinase.Gene')
cat('demo kinases:', nrow(s1), '| z(FC) = -z(1/FC) for all:', isTRUE(all.equal(mm$z.score.x, -mm$z.score.y)), '\n')

# 2) SYNTHETIC prior in the real layout
W <- 'F:/OpenScience/audits/bio-proteomics-ptm-analysis/rerun/in4_ksea'; dir.create(W, showWarnings = FALSE)
syn <- read.delim('F:/OpenScience/audits/bio-proteomics-ptm-analysis/data/phospho/kinase_substrate_SYNTHETIC.tsv')
truth <- read.csv('F:/OpenScience/audits/bio-proteomics-ptm-analysis/data/phospho/truth_sites.csv')
tmpl <- demoKS[rep(1, nrow(syn)), ]
tmpl$KINASE <- syn$KINASE; tmpl$GENE <- syn$KINASE; tmpl$KIN_ACC_ID <- paste0('K', seq_len(nrow(syn)))
tmpl$SUB_ACC_ID <- syn$SUB_ACC_ID; tmpl$SUB_GENE <- truth$gene[match(syn$SUB_ACC_ID, truth$protein)]
tmpl$SUB_MOD_RSD <- syn$SUB_MOD_RSD; tmpl$Source <- 'PhosphoSitePlus'
write.csv(tmpl, file.path(W, 'PSP&NetworKIN_Kinase_Substrate_Dataset.csv'), row.names = FALSE)
file.copy('F:/OpenScience/audits/bio-proteomics-ptm-analysis/data/phospho/proteinGroups_global.txt', file.path(W, 'proteinGroups_global.txt'), overwrite = TRUE)
cat('synthetic prior rows:', nrow(tmpl), '| kinases:', paste(unique(tmpl$KINASE), collapse = ', '), '\n')

# 3) the Skill block verbatim, in the session state the PTM block leaves (rd, adjusted)
rd <- function(f) read.table(f, sep = '\t', header = TRUE, quote = '')
adjusted <- readRDS('F:/OpenScience/audits/bio-proteomics-ptm-analysis/rerun/in1_result.rds')$adjusted
cat('adjusted Label:', unique(adjusted$Label), '\n')
blk <- ksea_block()
blk <- sub('library(KSEAapp)', '# library(KSEAapp)  [sourced from CRAN source instead; not installed]', blk, fixed = TRUE)
setwd(W)
eval(parse(text = blk), envir = globalenv())
cat('PX rows:', nrow(PX), '| Gene NA dropped ok:', all(!is.na(PX$Gene)), '\n')
print(kinase_scores[order(kinase_scores$z.score), c('Kinase.Gene', 'm', 'z.score', 'FDR')])
# expected direction from truth: substrates of each kinase, mean true occupancy change (Treatment - Control)
sub_truth <- merge(syn, truth, by.x = c('SUB_ACC_ID'), by.y = 'protein')
print(aggregate(true_occupancy_log2fc ~ KINASE, data = sub_truth, FUN = mean))
