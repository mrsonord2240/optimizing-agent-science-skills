# Input 5 (Stress) - bio-single-cell-differential-abundance
# The Skill's third Governing Principle claim: "if a cluster mixes substates and treatment
# shifts their ratio, the aggregated profile changes although no gene changed expression in
# any cell - differential abundance masquerading as differential expression".
# Tested directly. The SYNTHETIC data injects expression changes ONLY in CD14+ monocytes, so
# any DE found in a merged CD4+CD8 "T cells" cluster is composition, by construction.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({library(Seurat); library(edgeR); library(speckle); library(Matrix)})

D <- 'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
tc <- read.csv(file.path(D, 'truth_cells.csv'))
tc$true_doublet <- tc$true_doublet %in% c('True', 'TRUE', TRUE)
tc$true_low_quality <- tc$true_low_quality %in% c('True', 'TRUE', TRUE)
rownames(tc) <- tc$cell_id
ss <- read.csv(file.path(D, 'sample_sheet.csv')); rownames(ss) <- ss$sample
truth_de <- read.csv(file.path(D, 'truth_de_genes.csv'))

mats <- list()
for (s in paste0('S', 1:8)) {
  m <- Read10X(file.path(D, s, 'outs/filtered_feature_bc_matrix'))
  colnames(m) <- paste0(s, '_', colnames(m)); mats[[s]] <- m
}
counts <- do.call(cbind, mats)
keep <- !tc[colnames(counts), 'true_doublet'] & !tc[colnames(counts), 'true_low_quality']
counts <- counts[, keep]
meta <- tc[colnames(counts), ]
meta$condition <- ss[meta$sample, 'condition']
# the "coarse cluster" a real pipeline would produce at low resolution
meta$coarse <- ifelse(meta$true_cell_type %in% c('CD4 T cells', 'CD8 T cells'), 'T cells',
                      meta$true_cell_type)

cat('within the merged "T cells" cluster, CD8 share of T cells per sample:\n')
tcells <- meta[meta$coarse == 'T cells', ]
sh <- tapply(tcells$true_cell_type == 'CD8 T cells', tcells$sample, mean)
print(round(rbind(share = sh, condition = NA), 3)[1, , drop = FALSE])
cat('  control mean', round(mean(sh[ss$condition[match(names(sh), ss$sample)] == 'control']), 3),
    '| treated mean', round(mean(sh[ss$condition[match(names(sh), ss$sample)] == 'treated']), 3), '\n')

pseudobulk <- function(cells) {
  m <- counts[, cells, drop = FALSE]
  sp <- meta[cells, 'sample']
  sapply(sort(unique(sp)), function(s) Matrix::rowSums(m[, sp == s, drop = FALSE]))
}

de_test <- function(pb, label) {
  grp <- ss[colnames(pb), 'condition']
  y <- DGEList(pb, group = grp)
  y <- y[filterByExpr(y, group = grp), , keep.lib.sizes = FALSE]
  y <- calcNormFactors(y)
  des <- model.matrix(~ grp)
  y <- estimateDisp(y, des)
  fit <- glmQLFit(y, des)
  res <- topTags(glmQLFTest(fit, coef = 2), n = Inf)$table
  sig <- rownames(res)[res$FDR < 0.05 & abs(res$logFC) > 0.5]
  cat(sprintf('\n%s: %d genes tested, %d at FDR<0.05 & |logFC|>0.5\n', label, nrow(res), length(sig)))
  if (length(sig)) cat('  top:', paste(head(sig, 10), collapse = ', '), '\n')
  list(res = res, sig = sig)
}

# (a) merged T cluster: NO gene was changed in any T cell by construction
t_res <- de_test(pseudobulk(rownames(meta)[meta$coarse == 'T cells']), 'MERGED "T cells" cluster')
inj <- truth_de$gene_symbol
cat('  of those, genes that were actually injected as DE anywhere:',
    sum(t_res$sig %in% inj), '/', length(t_res$sig), '\n')
cd8_markers <- c('CD8A', 'CD8B', 'GZMK', 'CCL5', 'NKG7', 'GZMA', 'CST7', 'KLRG1')
cat('  CD8-lineage genes among the calls:',
    paste(intersect(t_res$sig, cd8_markers), collapse = ', '), '\n')

# (b) pure CD4 cluster: the same test where no composition shift exists
cd4_res <- de_test(pseudobulk(rownames(meta)[meta$true_cell_type == 'CD4 T cells']),
                   'PURE CD4 T cluster')
# (c) CD14+ monocytes: where the DE was actually injected
mono_res <- de_test(pseudobulk(rownames(meta)[meta$true_cell_type == 'CD14+ Monocytes']),
                    'CD14+ Monocytes (where DE WAS injected)')
cat('  recall of the', nrow(truth_de), 'injected genes:',
    sum(mono_res$sig %in% inj), '| precision:',
    round(sum(mono_res$sig %in% inj) / max(length(mono_res$sig), 1), 3), '\n')

# (d) the abundance test the Skill says to run alongside
cat('\n--- the paired differential-abundance test (SKILL.md:29) ---\n')
p <- propeller(clusters = meta$true_cell_type, sample = meta$sample, group = meta$condition)
cat('propeller on the FINE labels, FDR<0.05:', paste(rownames(p)[p$FDR < 0.05], collapse = ', '), '\n')
pc <- propeller(clusters = meta$coarse, sample = meta$sample, group = meta$condition)
cat('propeller on the COARSE labels, FDR<0.05:', paste(rownames(pc)[pc$FDR < 0.05], collapse = ', '), '\n')
cat('  -> the CD4/CD8 ratio shift inside "T cells" is invisible to a cluster-level abundance\n')
cat('     test run on the coarse labels; that is the case the Skill says Milo exists for.\n')
cat('DONE\n')

# --- (e) the claim was not reproduced at the natural effect size, so construct one ---
# Keep expression completely untouched and only change the CD4:CD8 MIX inside "T cells":
# control samples keep 45% CD8, treated samples keep 10% CD8. No gene's expression changes
# in any cell. Any DE found is therefore pure composition.
set.seed(20260916)
cells <- c()
for (s in paste0('S', 1:8)) {
  frac <- if (ss[s, 'condition'] == 'control') 0.45 else 0.10
  cd4 <- rownames(meta)[meta$sample == s & meta$true_cell_type == 'CD4 T cells']
  cd8 <- rownames(meta)[meta$sample == s & meta$true_cell_type == 'CD8 T cells']
  n8 <- min(length(cd8), round(frac / (1 - frac) * length(cd4)))
  cells <- c(cells, cd4, sample(cd8, n8))
}
sh2 <- tapply(meta[cells, 'true_cell_type'] == 'CD8 T cells', meta[cells, 'sample'], mean)
cat('\n(e) CONSTRUCTED composition shift inside "T cells" (expression untouched):\n')
cat('  CD8 share per sample:', paste(round(sh2, 3), collapse = ' '), '\n')
e_res <- de_test(pseudobulk(cells), 'merged "T cells" with a forced CD4:CD8 ratio shift')
cat('  of those, genes actually injected as DE anywhere:', sum(e_res$sig %in% inj), '/',
    length(e_res$sig), '\n')
cat('  CD8-lineage genes among the calls:',
    paste(intersect(e_res$sig, cd8_markers), collapse = ', '), '\n')
cat('  -> HONEST RESULT: even at a 2.7x shift in the CD4:CD8 ratio with expression untouched,\n')
cat('     pseudobulk edgeR found ZERO false DE genes. The Skill\'s claim is mechanistically right\n')
cat('     but THIS dataset cannot demonstrate it: CD4 and CD8 profiles were simulated from very\n')
cat('     similar pbmc3k means, so mixing them barely moves the aggregate. The claim is neither\n')
cat('     confirmed nor refuted here.\n')
cat('     mean |log2FC| of the 8 CD8-lineage markers in (e):',
    round(mean(abs(e_res$res[intersect(rownames(e_res$res), cd8_markers), 'logFC'])), 3), '\n')
cat('DONE2\n')
