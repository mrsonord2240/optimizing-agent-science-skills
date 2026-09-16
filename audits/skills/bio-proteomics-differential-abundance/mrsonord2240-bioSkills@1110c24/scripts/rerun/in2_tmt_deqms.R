# Input 2 (regression): two TMT10plex batches, PSM table, DEqMS with PSM counts. SYNTHETIC data.
source('F:/OpenScience/audits/bio-proteomics-differential-abundance/rerun/common.R')
psm <- read.csv(file.path(RR, 'data', 'tmt_psms.csv'), check.names = FALSE)
des <- read.csv(file.path(RR, 'data', 'tmt_psm_design.csv'), colClasses = 'character')
tr <- read.csv(file.path(RR, 'data', 'tmt_psm_truth.csv'))
truth <- data.frame(protein = tr$protein, class = tr$class)

# Agent's summarization (quantification step, needed only to build the matrix): per plex log2 ratio to 131, protein median
mats <- list(); counts <- list()
for (px in unique(des$plex)) {
  d <- des[des$plex == px & des$channel != '131', ]
  p <- psm[psm$plex == px, ]
  ref <- log2(p[['Abundance 131']])
  lr <- sapply(d$channel, function(ch) log2(p[[paste('Abundance', ch)]]) - ref)
  colnames(lr) <- d$sample
  agg <- aggregate(lr, by = list(protein = p$protein), FUN = median, na.rm = TRUE)
  rownames(agg) <- agg$protein
  m <- as.matrix(agg[, -1])
  if (!exists('NO_NORM')) m <- sweep(m, 2, apply(m, 2, median, na.rm = TRUE))   # channel median centering (loading)
  mats[[px]] <- m
  counts[[px]] <- table(p$protein)
}
common <- Reduce(intersect, lapply(mats, rownames))
protein_matrix <- do.call(cbind, lapply(mats, function(m) m[common, ]))
sample_info <- des[des$channel != '131', c('sample', 'condition', 'plex')]
names(sample_info)[3] <- 'batch'
protein_matrix <- protein_matrix[, sample_info$sample]
cat('proteins in both plexes:', nrow(protein_matrix), '| samples:', ncol(protein_matrix), '|', table(sample_info$condition), '\n')

run_block('b01')
cat('limma rows after filter:', nrow(fit2), '| df.prior:', round(median(fit2$df.prior), 2), '\n')
truth_eval(rownames(results)[results$adj.P.Val < 0.05], truth, 'limma trend+robust, plex as batch')
limma_res <- results

cnt <- do.call(cbind, lapply(counts, function(t) as.numeric(t[rownames(fit2)])))
psm_count_per_protein <- setNames(apply(cnt, 1, min), rownames(fit2))   # minimum across plexes, as the Skill directs
run_block('b03')
cat('DEqMS prior df:', round(fit3$sca.dfprior, 1), '\n')
truth_eval(rownames(results)[results$sca.adj.pval < 0.05], truth, 'DEqMS min PSM count sca.adj.pval<0.05')

psm_count_per_protein <- setNames(rowSums(cnt), rownames(fit2))
run_block('b03')
truth_eval(rownames(results)[results$sca.adj.pval < 0.05], truth, 'DEqMS SUM PSM count (not Skill) sca.adj.pval<0.05')
called <- rownames(limma_res)[limma_res$adj.P.Val < 0.05]
up <- called[tr$class[match(called, tr$protein)] == 'up']
cat('called up: median est logFC', round(median(limma_res[up, 'logFC']), 2), 'vs true', round(median(tr$true_log2fc[match(up, tr$protein)]), 2), '\n')
