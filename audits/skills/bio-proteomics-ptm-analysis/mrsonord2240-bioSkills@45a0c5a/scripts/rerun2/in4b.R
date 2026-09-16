
# Second independent check of the KSEA z-scores: recompute the Casado statistic using the
# whole-dataset mean/SD (which is what KSEA.Scores uses), not just the merged substrate rows.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages(library(KSEAapp))
W <- 'F:/OpenScience/audits/bio-proteomics-ptm-analysis/rerun2/work4'; setwd(W)
KSD <- read.csv('PSP&NetworKIN_Kinase_Substrate_Dataset.csv')
PXf <- read.csv('PX_used.csv')
mg <- merge(KSD[, c('GENE','SUB_GENE','SUB_MOD_RSD')], PXf,
            by.x = c('SUB_GENE','SUB_MOD_RSD'), by.y = c('Gene','Residue.Both'))
mg$l <- log2(mg$FC)
mu <- mean(log2(PXf$FC)); sdv <- sd(log2(PXf$FC))
hand <- do.call(rbind, lapply(split(mg, mg$GENE), function(d)
  data.frame(Kinase.Gene = d$GENE[1], m = nrow(d), z_hand_fullsd = (mean(d$l) - mu) * sqrt(nrow(d)) / sdv)))
pk <- KSEA.Scores(KSD, PXf, NetworKIN = FALSE, NetworKIN.cutoff = 3)
h <- merge(pk[, c('Kinase.Gene','z.score')], hand, by = 'Kinase.Gene')
print(h, row.names = FALSE)
cat('max |difference| using whole-dataset mean/SD:', signif(max(abs(h$z.score - h$z_hand_fullsd)), 3), '\n')
