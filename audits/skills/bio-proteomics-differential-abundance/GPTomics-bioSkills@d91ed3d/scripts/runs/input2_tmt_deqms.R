.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# INPUT 2 (Variant A): two TMT10plex batches, PSM table, DEqMS with PSM counts (min across plexes).
# Summarization (per-plex median sweep) is the quantification skill's territory; used here only to build the matrix.
suppressPackageStartupMessages({library(limma); library(DEqMS)})
D <- 'F:/OpenScience/audits/bio-proteomics-differential-abundance/data'
psm <- read.csv(file.path(D, 'tmt_psms.csv'), check.names = FALSE)
des <- read.csv(file.path(D, 'tmt_psm_design.csv'))
tru <- read.csv(file.path(D, 'tmt_psm_truth.csv')); rownames(tru) <- tru$protein
chan_cols <- grep('^Abundance', colnames(psm), value = TRUE)

# per-plex: log2 PSM reporter intensities -> ratio to the pooled reference (131) -> protein median
prot_mats <- list(); counts <- list()
for (p in c('A', 'B')) {
  x <- psm[psm$plex == p, ]
  l2 <- log2(as.matrix(x[, chan_cols]))
  rat <- l2[, setdiff(chan_cols, 'Abundance 131')] - l2[, 'Abundance 131']
  pm <- apply(rat, 2, function(v) tapply(v, x$protein, median))
  colnames(pm) <- des$sample[des$plex == p & des$channel != 131]
  pm <- sweep(pm, 2, apply(pm, 2, median))                    # equalize channel medians
  prot_mats[[p]] <- pm
  counts[[p]] <- table(x$protein)
}
prots <- sort(intersect(rownames(prot_mats$A), rownames(prot_mats$B)))
protein_matrix <- cbind(prot_mats$A[prots, ], prot_mats$B[prots, ])
sample_info <- des[match(colnames(protein_matrix), des$sample), ]
sample_info$condition <- factor(sample_info$condition, levels = c('Control', 'Treatment'))
sample_info$batch <- factor(sample_info$plex)
cat('Proteins quantified in both plexes:', length(prots), '| samples:', ncol(protein_matrix),
    '(', paste(table(sample_info$condition), collapse = ' C / '), 'T )\n')

# --- SKILL.md limma block (batch = plex as covariate)
design <- model.matrix(~0 + condition + batch, data = sample_info)  # batch in the model, not removed first
colnames(design)[1:2] <- levels(factor(sample_info$condition))
fit <- lmFit(protein_matrix, design)
contrast_matrix <- makeContrasts(Treatment - Control, levels = design)
fit2 <- contrasts.fit(fit, contrast_matrix)
fit2 <- eBayes(fit2, trend = TRUE, robust = TRUE)
cat('limma df.prior:', round(median(fit2$df.prior), 2), '\n')

# --- SKILL.md DEqMS block: PSM count, MINIMUM across batches
psm_count_per_protein <- pmin(as.numeric(counts$A[prots]), as.numeric(counts$B[prots])); names(psm_count_per_protein) <- prots
fit2$count <- psm_count_per_protein[rownames(fit2$coefficients)]  # PSM for TMT, peptide for LFQ; min across batches
fit3 <- spectraCounteBayes(fit2)
results <- outputResult(fit3, coef_col = 1)
cat('outputResult columns:', paste(colnames(results), collapse = ', '), '\n')
cat('DEqMS prior df:', fit3$sca.dfprior, '\n')

sc <- function(called, label) {
  cl <- tru[called, 'class']
  cat(sprintf('%-40s called=%3d  FP=%2d  realizedFDR=%4.1f%%  TP=%2d/80\n', label, length(called), sum(cl == 'null'),
              ifelse(length(called), 100 * mean(cl == 'null'), 0), sum(cl != 'null')))
}
sc(rownames(results)[results$sca.adj.pval < 0.05], 'DEqMS, min PSM count (Skill)')
sc(rownames(results)[results$adj.P.Val < 0.05], 'limma trend+robust (same fit)')
# alternative count choice the Skill warns about: total across batches
f2b <- fit2; f2b$count <- (as.numeric(counts$A[prots]) + as.numeric(counts$B[prots]))[match(rownames(f2b$coefficients), prots)]
rb <- outputResult(spectraCounteBayes(f2b), coef_col = 1)
sc(rownames(rb)[rb$sca.adj.pval < 0.05], 'DEqMS, SUM of PSM counts')
# do single-PSM proteins get false positives under limma but not DEqMS?
one <- names(psm_count_per_protein)[psm_count_per_protein == 1]
cat('Proteins with min PSM count = 1:', length(one), '| limma calls among them:', sum(results[one, 'adj.P.Val'] < 0.05),
    '(null:', sum(results[one, 'adj.P.Val'] < 0.05 & tru[one, 'class'] == 'null'), ') | DEqMS calls:',
    sum(results[one, 'sca.adj.pval'] < 0.05), '(null:', sum(results[one, 'sca.adj.pval'] < 0.05 & tru[one, 'class'] == 'null'), ')\n')
# variance vs count relationship DEqMS exploits
cat('Median residual SD by min-count bin:\n')
print(round(tapply(fit2$sigma, cut(psm_count_per_protein[rownames(fit2$coefficients)], c(0, 1, 2, 4, 8, 100)), median), 3))
cat('Compressed truth vs estimate for called up proteins (median):', round(median(results[rownames(results)[results$sca.adj.pval < 0.05 & results$logFC > 0], 'logFC']), 2),
    'vs true (uncompressed)', round(median(tru[rownames(results)[results$sca.adj.pval < 0.05 & results$logFC > 0], 'true_log2fc']), 2), '\n')
print(head(results[, c('logFC', 'count', 'sca.t', 'sca.P.Value', 'sca.adj.pval')], 8))
write.csv(results, 'F:/OpenScience/audits/bio-proteomics-differential-abundance/runs/input2_deqms_results.csv')
