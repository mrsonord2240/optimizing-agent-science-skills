# Follow-up to input 2: Milo with SKILL.md's prescribed k=30, prop=0.1 found ZERO significant
# neighbourhoods on a real 2.25x NK expansion with n=4/group. Can Milo find it at all with
# other settings, or is the dataset out of its range? This decides whether the finding is a
# defect in the Skill's numbers or a limitation of the method at this scale.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({
  library(miloR); library(SingleCellExperiment); library(Seurat); library(scater); library(dplyr)
})
D <- 'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
tc <- read.csv(file.path(D, 'truth_cells.csv'))
tc$true_doublet <- tc$true_doublet %in% c('True', 'TRUE', TRUE)
tc$true_low_quality <- tc$true_low_quality %in% c('True', 'TRUE', TRUE)
rownames(tc) <- tc$cell_id
ss <- read.csv(file.path(D, 'sample_sheet.csv')); rownames(ss) <- ss$sample
mats <- list()
for (s in paste0('S', 1:8)) {
  m <- Read10X(file.path(D, s, 'outs/filtered_feature_bc_matrix'))
  colnames(m) <- paste0(s, '_', colnames(m)); mats[[s]] <- m
}
counts <- do.call(cbind, mats)
counts <- counts[, !tc[colnames(counts), 'true_doublet'] & !tc[colnames(counts), 'true_low_quality']]
so <- CreateSeuratObject(counts, min.cells = 3, min.features = 200)
so$sample <- sub('_.*', '', colnames(so))
so$condition <- ss[so$sample, 'condition']
so$cell_type <- tc[colnames(so), 'true_cell_type']
set.seed(20260916)
so <- NormalizeData(so, verbose = FALSE); so <- FindVariableFeatures(so, verbose = FALSE)
so <- ScaleData(so, verbose = FALSE); so <- RunPCA(so, npcs = 50, verbose = FALSE)
sce <- as.SingleCellExperiment(so); reducedDim(sce, 'PCA') <- Embeddings(so, 'pca')[, 1:30]
design <- distinct(data.frame(colData(sce))[, c('sample', 'condition')])
rownames(design) <- design$sample
cat('cells per sample:', paste(table(sce$sample), collapse = ' '), '\n')
cat('NK cells per sample:', paste(table(sce$sample[sce$cell_type == 'NK cells']), collapse = ' '), '\n\n')

res <- list()
for (k in c(30, 50, 80, 120)) {
  m <- Milo(sce)
  m <- suppressMessages(buildGraph(m, k = k, d = 30, reduced.dim = 'PCA'))
  m <- suppressMessages(makeNhoods(m, prop = 0.2, k = k, d = 30, refined = TRUE, reduced_dims = 'PCA'))
  m <- suppressMessages(countCells(m, meta.data = as.data.frame(colData(m)), samples = 'sample'))
  m <- suppressMessages(calcNhoodDistance(m, d = 30, reduced.dim = 'PCA'))
  d <- suppressMessages(testNhoods(m, design = ~ condition, design.df = design, reduced.dim = 'PCA'))
  d <- suppressMessages(annotateNhoods(m, d, coldata_col = 'cell_type'))
  s <- d[d$SpatialFDR < 0.1, ]
  nkall <- d[d$cell_type == 'NK cells', ]
  cat(sprintf('k=%3d prop=0.20: %4d nhoods (median %3.0f cells) | sig %3d | NK sig %2d/%2d | '
              , k, nrow(d), median(colSums(nhoods(m))), nrow(s),
              sum(s$cell_type == 'NK cells'), nrow(nkall)))
  cat(sprintf('best NK: logFC %+.2f, p %.3g, SpatialFDR %.3g\n',
              nkall$logFC[which.min(nkall$PValue)], min(nkall$PValue), min(nkall$SpatialFDR)))
}
cat('DONE\n')
