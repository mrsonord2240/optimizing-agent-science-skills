.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# Re-audit 2026-09-15: why are KSEA z-scores NaN on the synthetic prior? Step through KSEA.Scores internals.
SP <- 'C:/Users/User/AppData/Local/Temp/claude/f--openscience-specialist-marketplace/5c5e1ac7-a797-41ee-9a87-111d2ea0f6a7/scratchpad/ksea/KSEAapp'
source(file.path(SP, 'R', 'KSEA.Scores.R')); load(file.path(SP, 'data', 'KSData.RData')); load(file.path(SP, 'data', 'PX.RData'))
s1 <- KSEA.Scores(KSData, PX, NetworKIN = FALSE); cat('demo z NaN count:', sum(is.nan(s1$z.score)), 'of', nrow(s1), '\n')
cat('class of demo KSData columns:', paste(sapply(KSData, class), collapse=','), '\n')
W <- 'F:/OpenScience/audits/bio-proteomics-ptm-analysis/rerun/in4_ksea'
KS <- read.csv(file.path(W, 'PSP&NetworKIN_Kinase_Substrate_Dataset.csv'))
adjusted <- readRDS('F:/OpenScience/audits/bio-proteomics-ptm-analysis/rerun/in1_result.rds')$adjusted
pg <- read.table(file.path(W, 'proteinGroups_global.txt'), sep = '\t', header = TRUE, quote = '')
gene_symbol <- setNames(sub(';.*', '', pg$Gene.names), sub(';.*', '', pg$Protein.IDs))
PX2 <- data.frame(Protein = sub('_[STY][0-9]+$', '', adjusted$Protein), Gene = gene_symbol[sub('_[STY][0-9]+$', '', adjusted$Protein)],
                  Peptide = 'NULL', Residue.Both = sub('^.*_', '', adjusted$Protein), p = adjusted$adj.pvalue, FC = 2^adjusted$log2FC)
PX2 <- PX2[!is.na(PX2$Gene) & is.finite(PX2$FC), ]
cat('PX2 p NA:', sum(is.na(PX2$p)), '| FC range', range(PX2$FC), '\n')
new <- PX2; colnames(new)[c(2,4)] <- c('SUB_GENE','SUB_MOD_RSD'); new$log2FC <- log2(abs(as.numeric(as.character(new$FC))))
cat('mean/sd new$log2FC:', mean(new$log2FC, na.rm=TRUE), sd(new$log2FC, na.rm=TRUE), '\n')
f <- KS[grep('PhosphoSitePlus', KS$Source), ]; d <- merge(f, new); cat('merged rows:', nrow(d), '| merged columns:', paste(names(d), collapse=','), '\n')
print(head(d[, c(5,1,2,16:19,14)]))
# second method: z by hand, Casado formula
km <- aggregate(log2FC ~ GENE, data = d, FUN = mean); km$m <- as.vector(table(d$GENE)[km$GENE])
km$z <- (km$log2FC - mean(new$log2FC)) * sqrt(km$m) / sd(new$log2FC); print(km)
# does a PX with p = NA rows break it? try p replaced by 'NULL'
PX3 <- PX2; PX3$p[is.na(PX3$p)] <- 'NULL'; s3 <- KSEA.Scores(KS, PX3, NetworKIN = FALSE); print(s3[, c('Kinase.Gene','m','z.score')])
