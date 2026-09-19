.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({
  library(Signac)
  library(Seurat)
  library(JASPAR2020)
  library(TFBSTools)
  library(motifmatchr)
  library(BSgenome.Hsapiens.UCSC.hg38)
  library(BiocParallel)
  library(chromVAR)
  library(SummarizedExperiment)
})
register(SerialParam())

data_dir <- 'F:/OpenScience/audits/bio-single-cell-scatac-analysis/data/reaudit_v2_20260919'
obj <- readRDS(file.path(data_dir, 'obj_qc.rds'))
cat('Loaded object:', ncol(obj), 'cells x', nrow(obj), 'peaks\n')
cat('chromVAR version:', as.character(packageVersion('chromVAR')), '\n')

pfm <- getMatrixSet(JASPAR2020, opts = list(collection = 'CORE', tax_group = 'vertebrates', all_versions = FALSE))
cat('PFMs fetched:', length(pfm), '\n')

DefaultAssay(obj) <- 'peaks'
obj <- AddMotifs(obj, genome = BSgenome.Hsapiens.UCSC.hg38, pfm = pfm)

# ---- EXACT block now in the fixed SKILL.md (chromVAR Motif Deviations section) ----
run_chromvar_block <- function(obj) {
  se <- SummarizedExperiment(assays = list(counts = as.matrix(GetAssayData(obj, assay = 'peaks', layer = 'counts'))),
                              rowRanges = granges(obj[['peaks']]))
  se <- addGCBias(se, genome = BSgenome.Hsapiens.UCSC.hg38)
  motif_ix <- matchMotifs(pfm, se, genome = BSgenome.Hsapiens.UCSC.hg38)
  bg_peaks <- getBackgroundPeaks(se)
  dev <- computeDeviations(object = se, annotations = motif_ix, background_peaks = bg_peaks)
  dev
}

cat('\n--- Run 1 of the SKILL.md chromVAR replacement block ---\n')
dev1 <- run_chromvar_block(obj)
z1 <- deviationScores(dev1)
cat('deviations dims (motifs x cells):', dim(dev1), '\n')
cat('any NA/NaN in z-scores?', any(is.na(z1)), '\n')
cat('z-score summary (sanity: should not be degenerate/all-zero):\n')
print(summary(as.vector(z1)))

obj[['chromvar']] <- CreateAssayObject(data = z1)
DefaultAssay(obj) <- 'chromvar'
diff_motifs <- FindMarkers(obj, ident.1 = 'Tcell', ident.2 = 'Bcell', group.by = 'cell_type',
                            mean.fxn = rowMeans, fc.name = 'avg_diff')
diff_motifs <- diff_motifs[order(diff_motifs$p_val_adj), ]
cat('Differential motifs Tcell vs Bcell (p_val_adj<0.05):', sum(diff_motifs$p_val_adj < 0.05), 'of', nrow(diff_motifs), '\n')
top_ids <- rownames(head(diff_motifs, 5))
motif_names <- sapply(pfm[top_ids], function(x) name(x))
cat('Top 5 differential motif TF identities (Tcell vs Bcell):\n'); print(motif_names)

# ---- Determinism check (T3): is getBackgroundPeaks/computeDeviations seeded? ----
# SKILL.md has no set.seed() anywhere in the chromVAR section. chromVAR's getBackgroundPeaks samples
# candidate background peaks by GC/accessibility bin (Mahalanobis-nearest-neighbor bins, not a random
# draw in the current implementation) -- verify empirically rather than trusting the docs.
cat('\n--- Determinism check: run the identical block a second time, same session, no seed set ---\n')
dev2 <- run_chromvar_block(obj)
z2 <- deviationScores(dev2)
cat('z-score matrices identical (identical()):', identical(z1, z2), '\n')
cat('max abs diff:', max(abs(z1 - z2)), '\n')
cat('all.equal:', isTRUE(all.equal(z1, z2)), '\n')

bg1 <- getBackgroundPeaks(SummarizedExperiment(assays = list(counts = as.matrix(GetAssayData(obj, assay='peaks', layer='counts'))), rowRanges = granges(obj[['peaks']])) |> (\(x) addGCBias(x, genome = BSgenome.Hsapiens.UCSC.hg38))())
bg2 <- getBackgroundPeaks(SummarizedExperiment(assays = list(counts = as.matrix(GetAssayData(obj, assay='peaks', layer='counts'))), rowRanges = granges(obj[['peaks']])) |> (\(x) addGCBias(x, genome = BSgenome.Hsapiens.UCSC.hg38))())
cat('getBackgroundPeaks() output identical across 2 calls:', identical(bg1, bg2), '\n')

cat('\nSTAGE 3 (v2, chromVAR + determinism) DONE\n')
