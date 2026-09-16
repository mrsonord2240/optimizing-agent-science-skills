# Input 4 (Variant B) - bio-single-cell-doublet-detection
# The legacy Seurat route exactly as SKILL.md:113-124 and examples/doubletfinder.R prescribe.
# Checks the API-drift claim (*_v3 names removed), the pK sweep, modelHomotypic, and accuracy
# against the SYNTHETIC ground truth on one lane (S2).
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({library(Seurat); library(DoubletFinder)})
cat('DoubletFinder', as.character(packageVersion('DoubletFinder')),
    '| Seurat', as.character(packageVersion('Seurat')), '\n')

# the Skill says the *_v3 names were removed - check what this install actually exposes
fns <- ls('package:DoubletFinder')
cat('exported:', paste(fns, collapse = ', '), '\n')
cat('paramSweep present:', 'paramSweep' %in% fns, '| paramSweep_v3 present:', 'paramSweep_v3' %in% fns, '\n')
cat('doubletFinder present:', 'doubletFinder' %in% fns, '| doubletFinder_v3 present:',
    'doubletFinder_v3' %in% fns, '\n')

D <- 'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
tc <- read.csv(file.path(D, 'truth_cells.csv'))
tc$true_doublet <- tc$true_doublet %in% c('True', 'TRUE', 'true', TRUE)
tc <- tc[tc$sample == 'S2', ]; rownames(tc) <- tc$barcode

counts <- Read10X(file.path(D, 'S2/outs/filtered_feature_bc_matrix'))
seurat_obj <- CreateSeuratObject(counts = counts, min.cells = 3, min.features = 200)
cat('Loaded', ncol(seurat_obj), 'cells\n')
set.seed(20260916)
seurat_obj <- NormalizeData(seurat_obj, verbose = FALSE)
seurat_obj <- FindVariableFeatures(seurat_obj, verbose = FALSE)
seurat_obj <- ScaleData(seurat_obj, verbose = FALSE)
seurat_obj <- RunPCA(seurat_obj, verbose = FALSE)
seurat_obj <- FindNeighbors(seurat_obj, dims = 1:20, verbose = FALSE)
seurat_obj <- FindClusters(seurat_obj, resolution = 0.5, verbose = FALSE)

t0 <- Sys.time()
sweep.res <- paramSweep(seurat_obj, PCs = 1:20, sct = FALSE)
sweep.stats <- summarizeSweep(sweep.res, GT = FALSE)
bcmvn <- find.pK(sweep.stats)
optimal_pk <- as.numeric(as.character(bcmvn$pK[which.max(bcmvn$BCmetric)]))
cat('paramSweep +find.pK took', round(as.numeric(difftime(Sys.time(), t0, units = 'secs')), 1),
    's; optimal pK =', optimal_pk, '\n')

rate <- 0.008 * ncol(seurat_obj) / 1000
nExp_poi <- round(rate * ncol(seurat_obj))
homo <- modelHomotypic(seurat_obj$seurat_clusters)
nExp <- round(nExp_poi * (1 - homo))
cat('rate =', round(rate, 5), '| nExp before homotypic adjustment =', nExp_poi,
    '| modelHomotypic =', round(homo, 3), '| nExp =', nExp, '\n')
cat('TRUE doublets in this lane:', sum(tc[colnames(seurat_obj), 'true_doublet']), '\n')

# examples/doubletfinder.R:36 passes reuse.pANN = FALSE. Try that first, verbatim.
r <- try(doubletFinder(seurat_obj, PCs = 1:20, pN = 0.25, pK = optimal_pk,
                       nExp = nExp, reuse.pANN = FALSE, sct = FALSE), silent = TRUE)
if (inherits(r, 'try-error')) {
  cat('EXAMPLE SCRIPT CALL (reuse.pANN = FALSE) FAILED:\n  ', as.character(r))
  cat('  -> reuse.pANN = FALSE is not NULL, so doubletFinder takes its reuse branch:\n',
      '     pANN.old <- seu@meta.data[, FALSE] is a zero-column data.frame, then order() on it.\n')
} else { cat('example-script call succeeded\n'); seurat_obj <- r }
# SKILL.md:123 omits reuse.pANN entirely (default NULL). Try that.
seurat_obj <- doubletFinder(seurat_obj, PCs = 1:20, pN = 0.25, pK = optimal_pk,
                            nExp = nExp, sct = FALSE)
df_col <- grep('DF.classifications', colnames(seurat_obj@meta.data), value = TRUE)
pann_col <- grep('^pANN', colnames(seurat_obj@meta.data), value = TRUE)
cat('metadata column added:', df_col, '\n')
pred <- seurat_obj@meta.data[[df_col]] == 'Doublet'
truth <- tc[colnames(seurat_obj), 'true_doublet']
tp <- sum(pred & truth); fp <- sum(pred & !truth); fn <- sum(!pred & truth)
cat(sprintf('DoubletFinder: called %d  TP=%d FP=%d FN=%d recall=%.3f precision=%.3f\n',
            sum(pred), tp, fp, fn, tp / max(tp + fn, 1), tp / max(tp + fp, 1)))
rk <- rank(seurat_obj@meta.data[[pann_col]]); n1 <- sum(truth); n0 <- sum(!truth)
cat('AUC of pANN vs truth:', round((sum(rk[truth]) - n1 * (n1 + 1) / 2) / (n1 * n0), 4), '\n')

# what happens if nExp is set from the true rate instead of the Skill's rule
nExp_true <- round(sum(truth) * (1 - homo))
seurat_obj <- doubletFinder(seurat_obj, PCs = 1:20, pN = 0.25, pK = optimal_pk,
                            nExp = nExp_true, reuse.pANN = pann_col, sct = FALSE)
df2 <- tail(grep('DF.classifications', colnames(seurat_obj@meta.data), value = TRUE), 1)
p2 <- seurat_obj@meta.data[[df2]] == 'Doublet'
cat(sprintf('same pANN, nExp from the TRUE rate (%d): called %d recall=%.3f precision=%.3f\n',
            nExp_true, sum(p2), sum(p2 & truth) / max(sum(truth), 1), sum(p2 & truth) / max(sum(p2), 1)))
cat('DONE\n')
