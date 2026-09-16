
# RE-AUDIT B, PTM Input 4 (Variant B, regression of the pass-2 P1 fix): kinase activity with the
# SKILL.md KSEAapp block VERBATIM from the fork. KSEAapp 2.0 is now INSTALLED in the candidate R-lib,
# so the block runs with its own library() line intact - nothing is sourced from a scratchpad.
# Prior: the SYNTHETIC kinase-substrate table rebuilt in the real 14-column PSP&NetworKIN layout.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
source('F:/OpenScience/audits/bio-proteomics-ptm-analysis/rerun/skillblock.R')
RR <- 'F:/OpenScience/audits/bio-proteomics-ptm-analysis/rerun2'
W  <- file.path(RR, 'work4')
suppressPackageStartupMessages(library(KSEAapp))
cat('KSEAapp', as.character(packageVersion('KSEAapp')), '(installed, not sourced)\n')

# --- 1) sign behaviour on the package's own demo data, as a control -----------------
data(KSData); data(PX)
demoKS <- KSData; demoPX <- PX
s1 <- KSEA.Scores(demoKS, demoPX, NetworKIN = FALSE)
inv <- demoPX; inv$FC <- 1 / as.numeric(as.character(inv$FC))
s2 <- KSEA.Scores(demoKS, inv, NetworKIN = FALSE)
mm <- merge(s1[, c('Kinase.Gene','z.score')], s2[, c('Kinase.Gene','z.score')], by = 'Kinase.Gene')
cat('demo kinases:', nrow(s1), '| NaN z on demo:', sum(is.nan(s1$z.score)),
    '| z(FC) = -z(1/FC) for all:', isTRUE(all.equal(mm$z.score.x, -mm$z.score.y)), '\n')

# --- 2) build the synthetic prior in the real PSP&NetworKIN layout ------------------
dir.create(W, showWarnings = FALSE, recursive = TRUE)
D <- 'F:/OpenScience/audits/bio-proteomics-ptm-analysis/data/phospho'
syn   <- read.delim(file.path(D, 'kinase_substrate_SYNTHETIC.tsv'))
truth <- read.csv(file.path(D, 'truth_sites.csv'))
tmpl <- demoKS[rep(1, nrow(syn)), ]
tmpl$KINASE <- syn$KINASE; tmpl$GENE <- syn$KINASE; tmpl$KIN_ACC_ID <- paste0('K', seq_len(nrow(syn)))
tmpl$SUB_ACC_ID <- syn$SUB_ACC_ID; tmpl$SUB_GENE <- truth$gene[match(syn$SUB_ACC_ID, truth$protein)]
tmpl$SUB_MOD_RSD <- syn$SUB_MOD_RSD; tmpl$Source <- 'PhosphoSitePlus'
write.csv(tmpl, file.path(W, 'PSP&NetworKIN_Kinase_Substrate_Dataset.csv'), row.names = FALSE)
file.copy(file.path(D, 'proteinGroups_global.txt'), file.path(W, 'proteinGroups_global.txt'), overwrite = TRUE)
cat('synthetic prior rows:', nrow(tmpl), '| kinases:', paste(unique(tmpl$KINASE), collapse = ', '), '\n')

# --- 3) the Skill block VERBATIM, in the session state the PTM block leaves ----------
rd <- function(f) read.table(f, sep = '\t', header = TRUE, quote = '')
adjusted <- readRDS(file.path(RR, 'in1_result.rds'))$adjusted
cat('adjusted Label:', unique(adjusted$Label), '| ADJUSTED rows:', nrow(adjusted),
    '| non-finite log2FC rows present:', sum(!is.finite(adjusted$log2FC)), '\n')
setwd(W)
blk <- ksea_block()
cat('block still contains library(KSEAapp):', grepl('library(KSEAapp)', blk, fixed = TRUE), '\n')
eval(parse(text = blk), envir = globalenv())
write.csv(PX, file.path(W,'PX_used.csv'), row.names=FALSE)
cat('PX rows:', nrow(PX), '| any non-finite FC in PX:', any(!is.finite(PX$FC)),
    '| any FC == 0 in PX:', any(PX$FC == 0), '\n')
cat('kinases scored:', nrow(kinase_scores), '| NaN z.scores:', sum(is.nan(kinase_scores$z.score)), '\n')
print(kinase_scores[order(kinase_scores$z.score), c('Kinase.Gene','m','z.score','p.value','FDR')])

# --- 4) do we KNOW the answer? compare against truth -------------------------------
sub_truth <- merge(syn, truth, by.x = 'SUB_ACC_ID', by.y = 'protein')
tr <- aggregate(true_occupancy_log2fc ~ KINASE, data = sub_truth, FUN = mean)
names(tr)[2] <- 'true_mean_occupancy_log2FC'
cmp <- merge(kinase_scores[, c('Kinase.Gene','m','z.score','FDR')], tr, by.x = 'Kinase.Gene', by.y = 'KINASE')
cmp$sign_agrees <- sign(cmp$z.score) == sign(cmp$true_mean_occupancy_log2FC)
cat('\n--- KSEA z-score vs known truth ---\n'); print(cmp, row.names = FALSE)
cat('sign agreement:', sum(cmp$sign_agrees), '/', nrow(cmp),
    '| rank correlation with truth:', round(cor(cmp$z.score, cmp$true_mean_occupancy_log2FC, method = 'spearman'), 3), '\n')

# --- 5) independent check: hand-computed Casado z-score on the merged table ---------
KSD <- read.csv('PSP&NetworKIN_Kinase_Substrate_Dataset.csv')
mg <- merge(KSD[, c('GENE','SUB_GENE','SUB_MOD_RSD')], PX,
            by.x = c('SUB_GENE','SUB_MOD_RSD'), by.y = c('Gene','Residue.Both'))
mg$log2FC <- log2(as.numeric(as.character(mg$FC)))
mu <- mean(mg$log2FC); sdv <- sd(mg$log2FC)
hand <- do.call(rbind, lapply(split(mg, mg$GENE), function(d)
  data.frame(Kinase.Gene = d$GENE[1], m = nrow(d),
             z_hand = (mean(d$log2FC) - mu) * sqrt(nrow(d)) / sdv)))
h <- merge(kinase_scores[, c('Kinase.Gene','z.score')], hand, by = 'Kinase.Gene')
cat('\nindependent hand-computed Casado z vs package z:\n'); print(h, row.names = FALSE)
cat('max |difference|:', signif(max(abs(h$z.score - h$z_hand)), 3), '\n')

# --- 6) the pre-fix PX filter, on the same data, for comparison --------------------
PXold <- data.frame(Protein = sub('_[STY][0-9]+$', '', adjusted$Protein),
                    Gene = gene_symbol[sub('_[STY][0-9]+$', '', adjusted$Protein)],
                    Peptide = 'NULL', Residue.Both = sub('^.*_', '', adjusted$Protein),
                    p = adjusted$adj.pvalue, FC = 2^adjusted$log2FC)
PXold <- PXold[!is.na(PXold$Gene) & is.finite(PXold$FC), ]
oldsc <- KSEA.Scores(KSD, PXold, NetworKIN = FALSE, NetworKIN.cutoff = 3)
cat('\nPRE-FIX filter (is.finite(FC)) on the same data: PX rows', nrow(PXold),
    '| FC == 0 rows kept:', sum(PXold$FC == 0), '| NaN z.scores:', sum(is.nan(oldsc$z.score)), '/', nrow(oldsc), '\n')
