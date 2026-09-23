# Input 2 (Variant A) - bio-single-cell-differential-abundance
# Milo exactly as SKILL.md:79-96, including annotateNhoods and the SpatialFDR report.
# SYNTHETIC 8-sample PBMC set; ground truth is an NK expansion (6% -> ~13%) and nothing else.
# Also exercises SKILL.md:53-58, the batch-adjusted design.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({
  library(miloR); library(SingleCellExperiment); library(Seurat); library(scater); library(dplyr)
})
cat('miloR', as.character(packageVersion('miloR')), '\n')

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
so$batch <- ss[so$sample, 'batch']
so$cell_type <- tc[colnames(so), 'true_cell_type']
set.seed(20260916)
so <- NormalizeData(so, verbose = FALSE); so <- FindVariableFeatures(so, verbose = FALSE)
so <- ScaleData(so, verbose = FALSE); so <- RunPCA(so, npcs = 50, verbose = FALSE)
sce <- as.SingleCellExperiment(so)
reducedDim(sce, 'PCA') <- Embeddings(so, 'pca')[, 1:30]
cat(ncol(sce), 'cells; PCA', paste(dim(reducedDim(sce, 'PCA')), collapse = ' x '), '\n')

# --- SKILL.md:83-95, verbatim ---
t0 <- Sys.time()
milo <- Milo(sce)
milo <- buildGraph(milo, k = 30, d = 30, reduced.dim = 'PCA')
milo <- makeNhoods(milo, prop = 0.1, k = 30, d = 30, refined = TRUE, reduced_dims = 'PCA')
milo <- countCells(milo, meta.data = as.data.frame(colData(milo)), samples = 'sample')
cat('neighbourhoods:', ncol(nhoods(milo)),
    '| median cells per nhood:', median(colSums(nhoods(milo))), '\n')

design <- data.frame(colData(milo))[, c('sample', 'condition', 'batch')]
design <- distinct(design)
rownames(design) <- design$sample
milo <- calcNhoodDistance(milo, d = 30, reduced.dim = 'PCA')
da <- testNhoods(milo, design = ~ condition, design.df = design, reduced.dim = 'PCA')
da <- annotateNhoods(milo, da, coldata_col = 'cell_type')
cat('testNhoods + annotateNhoods took',
    round(as.numeric(difftime(Sys.time(), t0, units = 'secs')), 1), 's\n')
cat('columns returned:', paste(colnames(da), collapse = ', '), '\n')

cat('\nSpatialFDR < 0.1 by annotated cell type (SKILL.md:95):\n')
print(table(da$SpatialFDR < 0.1, da$cell_type))
sig <- da[da$SpatialFDR < 0.1, ]
cat('\nsignificant neighbourhoods:', nrow(sig), 'of', nrow(da), '\n')
cat('direction by cell type (mean logFC among significant nhoods, treated vs control):\n')
print(round(tapply(sig$logFC, sig$cell_type, mean), 3))
cat('\nGROUND TRUTH: NK cells 6% -> ~13%; nothing else changed.\n')
cat('mixed-annotation neighbourhoods (cell_type_fraction < 0.7):',
    sum(da$cell_type_fraction < 0.7), 'of', nrow(da),
    '- the Skill calls these genuinely transitional, not errors\n')

# --- raw p vs SpatialFDR, the correction the Skill insists on reporting ---
cat(sprintf('\nraw PValue < 0.05: %d nhoods | FDR < 0.1: %d | SpatialFDR < 0.1: %d\n',
            sum(da$PValue < 0.05), sum(da$FDR < 0.1), sum(da$SpatialFDR < 0.1)))

# --- SKILL.md:53-58, the batch-adjusted design ---
da2 <- testNhoods(milo, design = ~ batch + condition, design.df = design, reduced.dim = 'PCA')
da2 <- annotateNhoods(milo, da2, coldata_col = 'cell_type')
cat('\nwith design = ~ batch + condition:\n')
print(table(da2$SpatialFDR < 0.1, da2$cell_type))
cat('agreement with the unadjusted call:',
    sum((da$SpatialFDR < 0.1) == (da2$SpatialFDR < 0.1)), '/', nrow(da), 'neighbourhoods\n')

# --- the Skill's k/prop sensitivity warning ---
cat('\nk / prop sensitivity (SKILL.md:98 "results sensitive to k and prop"):\n')
for (k in c(15, 30)) for (pr in c(0.05, 0.1)) {
  m2 <- Milo(sce)
  m2 <- buildGraph(m2, k = k, d = 30, reduced.dim = 'PCA')
  m2 <- makeNhoods(m2, prop = pr, k = k, d = 30, refined = TRUE, reduced_dims = 'PCA')
  m2 <- countCells(m2, meta.data = as.data.frame(colData(m2)), samples = 'sample')
  m2 <- calcNhoodDistance(m2, d = 30, reduced.dim = 'PCA')
  d2 <- testNhoods(m2, design = ~ condition, design.df = design, reduced.dim = 'PCA')
  d2 <- annotateNhoods(m2, d2, coldata_col = 'cell_type')
  s2 <- d2[d2$SpatialFDR < 0.1, ]
  nk <- sum(s2$cell_type == 'NK cells')
  cat(sprintf('  k=%2d prop=%.2f: %4d nhoods, %3d significant, %3d of them NK (%.0f%%)\n',
              k, pr, nrow(d2), nrow(s2), nk, 100 * nk / max(nrow(s2), 1)))
}
cat('DONE\n')
