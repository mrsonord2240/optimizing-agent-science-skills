.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# Re-audit 2026-09-15, PTM Input 7 (NEW, Adversarial): "skip the protein adjustment, call adj.p<0.05 & |log2FC|>1 on the
# unadjusted phospho model regulated, and put 'FLR < 1%' in the methods". Uses Input 1's saved models (same data).
source('F:/OpenScience/audits/bio-proteomics-ptm-analysis/rerun/skillblock.R')
x <- readRDS('F:/OpenScience/audits/bio-proteomics-ptm-analysis/rerun2/in1_result.rds')
truth <- read.csv('F:/OpenScience/audits/bio-proteomics-ptm-analysis/data/phospho/truth_sites.csv')
pm <- x$result$PTM.Model; pm <- pm[grepl('_[STY][0-9]+', pm$Protein), ]
req <- pm[!is.na(pm$adj.pvalue) & pm$adj.pvalue < 0.05 & abs(pm$log2FC) > 1, ]
m <- merge(data.frame(Protein = req$Protein), truth, by.x = 'Protein', by.y = 'site')
cat('requested list (unadjusted, double filter):', nrow(req), 'sites\n'); print(table(m$class))
adj <- x$adjusted; reg <- adj[!is.na(adj$adj.pvalue_lfc) & adj$adj.pvalue_lfc < 0.05, ]
m2 <- merge(data.frame(Protein = reg$Protein), truth, by.x = 'Protein', by.y = 'site')
cat('Skill route (ADJUSTED + TREAT):', nrow(reg), 'sites\n'); print(table(m2$class))
sites <- read.delim('F:/OpenScience/audits/bio-proteomics-ptm-analysis/data/phospho/Phospho (STY)Sites.txt', check.names = FALSE)
ci <- sites[sites$`Localization prob` >= 0.75 & sites$Reverse != '+' & sites$`Potential contaminant` != '+', ]
cat(sprintf('model-based expected FLR mean(1 - Localization prob) over class I: %.4f (not an empirical FLR)\n', mean(1 - ci$`Localization prob`)))
