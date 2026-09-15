.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# Input 2 (Variant A) - iq::maxLFQ (SKILL.md lines 98-104) vs MSstats TMP (Input 1) sensitivity on evidence.txt
setwd('F:/OpenScience/audits/bio-proteomics-quantification/data')
suppressPackageStartupMessages(library(iq))
cat('iq', as.character(packageVersion('iq')), '\n')
ev <- read.table('evidence.txt', sep = '\t', header = TRUE, quote = '', comment.char = '')   # quote-safe read (see Input 1)
ev <- ev[!(ev$Reverse %in% '+') & !(ev$Potential.contaminant %in% '+'), ]
ev$feature <- paste(ev$Modified.sequence, ev$Charge, sep = '_')
runs <- c('C1', 'C2', 'C3', 'C4', 'T1', 'T2', 'T3', 'T4')
ev$log2I <- log2(ev$Intensity); ev$log2I[!is.finite(ev$log2I)] <- NA

pep_matrix <- function(d) {       # rows = peptide ions, columns = samples, log2 (max per feature x run, as MSstats does)
  a <- tapply(d$log2I, list(d$feature, factor(d$Raw.file, levels = runs)), max)
  a[, runs, drop = FALSE]
}
## --- the Skill's block for ONE protein group
one <- 'O10000'
peptide_log2_matrix <- pep_matrix(ev[ev$Leading.razor.protein == one, ])
cat('\nONE protein', one, ':', nrow(peptide_log2_matrix), 'peptide ions x', ncol(peptide_log2_matrix), 'runs\n')
result <- maxLFQ(peptide_log2_matrix)
cat('names(result):', paste(names(result), collapse = ', '), '\n')
protein_estimate <- result$estimate    # one MaxLFQ value per sample
print(round(setNames(protein_estimate, runs), 3)); cat('annotation: "', result$annotation, '"\n', sep = '')

## --- all proteins, as the Skill's block is written (no normalization step before maxLFQ)
run_all <- function(d) {
  prots <- sort(unique(d$Leading.razor.protein))
  out <- t(sapply(prots, function(p) { m <- pep_matrix(d[d$Leading.razor.protein == p, ]); r <- maxLFQ(m); r$estimate }))
  colnames(out) <- runs; out
}
mlfq <- run_all(ev)
cat('\nMaxLFQ matrix:', nrow(mlfq), 'proteins; NA cells:', sum(is.na(mlfq)), '\n')
loadoff <- c(C1 = 0.10, C2 = -0.20, C3 = 0.15, C4 = 0.00, T1 = -0.10, T2 = 0.20, T3 = -0.15, T4 = 0.05)   # generator LOAD
ctr <- function(m) { md <- apply(m, 2, median, na.rm = TRUE); md - mean(md) }
cat('per-run median (centred) of maxLFQ estimates, NO pre-normalization:\n'); print(round(ctr(mlfq), 3))
cat('generator loading offsets (centred):\n'); print(round(loadoff - mean(loadoff), 3))

## --- adaptation: median-normalize peptide log2 per run first (what iq::preprocess does), then maxLFQ
ev2 <- ev; med <- tapply(ev2$log2I, ev2$Raw.file, median, na.rm = TRUE)
ev2$log2I <- ev2$log2I - med[ev2$Raw.file] + mean(med)
mlfq_n <- run_all(ev2)
cat('per-run median (centred), WITH per-run median normalization first:\n'); print(round(ctr(mlfq_n), 3))

## --- sensitivity vs TMP (Input 1, quote-safe run)
pa <- as.data.frame(readRDS('F:/OpenScience/audits/bio-proteomics-quantification/runs/in1_protein_level.rds'))
tmp <- tapply(pa$LogIntensities, list(sub(';.*', '', as.character(pa$Protein)), as.character(pa$originalRUN)), identity)
tmp <- tmp[, runs]
truth <- read.csv('truth_proteins.csv'); tr <- setNames(truth$true_log2fc, truth$protein); cls <- setNames(truth$class, truth$protein)
fc <- function(m) rowMeans(m[, 5:8], na.rm = TRUE) - rowMeans(m[, 1:4], na.rm = TRUE)
common <- intersect(rownames(tmp), rownames(mlfq_n))
common <- common[cls[common] != 'on_off']
f_tmp <- fc(tmp[common, ]); f_mlq <- fc(mlfq_n[common, ]); f_raw <- fc(mlfq[common, ])
ok <- is.finite(f_tmp) & is.finite(f_mlq)
cat(sprintf('\n%d shared non-on/off proteins with finite FC in both\n', sum(ok)))
cat(sprintf('corr with truth: TMP %.3f | MaxLFQ(normalized) %.3f | MaxLFQ(as Skill, unnormalized) %.3f\n',
            cor(f_tmp[ok], tr[common][ok]), cor(f_mlq[ok], tr[common][ok]), cor(f_raw[ok], tr[common][ok])))
cat(sprintf('RMSE vs truth: TMP %.3f | MaxLFQ(normalized) %.3f | MaxLFQ(unnormalized) %.3f\n',
            sqrt(mean((f_tmp - tr[common])[ok]^2)), sqrt(mean((f_mlq - tr[common])[ok]^2)), sqrt(mean((f_raw - tr[common])[ok]^2))))
d <- f_mlq - f_tmp
cat(sprintf('|FC(MaxLFQ) - FC(TMP)|: median %.3f, >0.5 log2 in %d proteins, >1 in %d\n', median(abs(d[ok])), sum(abs(d[ok]) > 0.5), sum(abs(d[ok]) > 1)))
big <- names(sort(abs(d[ok]), decreasing = TRUE))[1:5]
print(data.frame(protein = big, class = cls[big], truth = round(tr[big], 2), TMP = round(f_tmp[big], 2), MaxLFQ = round(f_mlq[big], 2),
                 n_features = sapply(big, function(p) length(unique(ev$feature[ev$Leading.razor.protein == p])))), row.names = FALSE)
# single-peptide / one-feature proteins: where the two diverge by construction
nfeat <- sapply(common, function(p) length(unique(ev$feature[ev$Leading.razor.protein == p])))
cat(sprintf('median |dFC| for proteins with <=2 features: %.3f (n=%d) vs >=5 features: %.3f (n=%d)\n',
            median(abs(d[ok & nfeat <= 2])), sum(ok & nfeat <= 2), median(abs(d[ok & nfeat >= 5])), sum(ok & nfeat >= 5)))
# disconnected sample graphs reported by maxLFQ
ann <- sapply(sort(unique(ev2$Leading.razor.protein)), function(p) maxLFQ(pep_matrix(ev2[ev2$Leading.razor.protein == p, ]))$annotation)
cat('proteins with a non-empty maxLFQ annotation (disconnected samples):', sum(ann != ''), '\n')
## bias diagnostics: DE composition of this 300-protein subset and mean FC error per method
cat('\nclass counts among evidence proteins:\n'); print(table(cls[unique(ev$Leading.razor.protein)]))
cat(sprintf('mean(FC - truth): TMP %+.3f | MaxLFQ(normalized) %+.3f | MaxLFQ(unnormalized) %+.3f\n',
            mean((f_tmp - tr[common])[ok]), mean((f_mlq - tr[common])[ok]), mean((f_raw - tr[common])[ok])))
nul <- ok & cls[common] == 'null'
cat(sprintf('null proteins only (n=%d) mean FC: TMP %+.3f | MaxLFQ(normalized) %+.3f | MaxLFQ(unnormalized) %+.3f\n',
            sum(nul), mean(f_tmp[nul]), mean(f_mlq[nul]), mean(f_raw[nul])))
