# Input 6 (Scope Boundary): exact repaired inline Milo block from SKILL.md at
# e986b98c85b38b4ad31ee9289f5aa39f6bec212b, after constructing its documented SCE input.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages(library(Seurat))
suppressPackageStartupMessages(library(scater))

d <- 'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
truth <- read.csv(file.path(d, 'truth_cells.csv'))
truth$true_doublet <- truth$true_doublet %in% c('True', 'TRUE', TRUE)
truth$true_low_quality <- truth$true_low_quality %in% c('True', 'TRUE', TRUE)
rownames(truth) <- truth$cell_id
sheet <- read.csv(file.path(d, 'sample_sheet.csv')); rownames(sheet) <- sheet$sample
mats <- lapply(paste0('S', 1:8), function(s) {
  x <- Read10X(file.path(d, s, 'outs/filtered_feature_bc_matrix'))
  colnames(x) <- paste0(s, '_', colnames(x)); x
})
counts <- do.call(cbind, mats)
keep <- !truth[colnames(counts), 'true_doublet'] & !truth[colnames(counts), 'true_low_quality']
counts <- counts[, keep]
so <- CreateSeuratObject(counts, min.cells = 3, min.features = 200)
so$sample <- sub('_.*', '', colnames(so))
so$condition <- sheet[so$sample, 'condition']
so$cell_type <- truth[colnames(so), 'true_cell_type']
set.seed(20260923)
so <- NormalizeData(so, verbose = FALSE)
so <- FindVariableFeatures(so, verbose = FALSE)
so <- ScaleData(so, verbose = FALSE)
so <- RunPCA(so, npcs = 50, verbose = FALSE)
sce <- as.SingleCellExperiment(so)
reducedDim(sce, 'PCA') <- Embeddings(so, 'pca')[, 1:30]

# --- exact repaired SKILL.md inline block ---
library(miloR)
library(SingleCellExperiment)
library(dplyr)

set.seed(42)
milo <- Milo(sce)
milo <- buildGraph(milo, k = 30, d = 30, reduced.dim = 'PCA')
milo <- makeNhoods(milo, prop = 0.1, k = 30, d = 30, refined = TRUE, reduced_dims = 'PCA')
milo <- countCells(milo, meta.data = as.data.frame(colData(milo)), samples = 'sample')

design <- data.frame(colData(milo))[, c('sample', 'condition')]
design <- distinct(design)
rownames(design) <- design$sample
milo <- calcNhoodDistance(milo, d = 30, reduced.dim = 'PCA')

da <- testNhoods(milo, design = ~ condition, design.df = design, reduced.dim = 'PCA')
da <- annotateNhoods(milo, da, coldata_col = 'cell_type')
tab <- table(da$SpatialFDR < 0.1, da$cell_type)
print(tab)
stopifnot(nrow(design) == 8L, nrow(da) > 0L, 'SpatialFDR' %in% colnames(da))
cat('PASS_MILO_INLINE_FULL_PATH designs=', nrow(design), ' neighbourhoods=', nrow(da), '\n', sep = '')
