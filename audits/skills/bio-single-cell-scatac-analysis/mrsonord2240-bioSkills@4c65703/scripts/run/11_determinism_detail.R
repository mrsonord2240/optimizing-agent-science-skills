.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({
  library(Signac); library(Seurat); library(JASPAR2020); library(TFBSTools)
  library(motifmatchr); library(BSgenome.Hsapiens.UCSC.hg38); library(BiocParallel)
  library(chromVAR); library(SummarizedExperiment)
})
register(SerialParam())

cat('--- Does getBackgroundPeaks() / computeDeviations() expose a seed argument? ---\n')
print(args(getBackgroundPeaks))
print(args(computeDeviations))

data_dir <- 'F:/OpenScience/audits/bio-single-cell-scatac-analysis/data/reaudit_v2_20260919'
obj <- readRDS(file.path(data_dir, 'obj_qc.rds'))
pfm <- getMatrixSet(JASPAR2020, opts = list(collection = 'CORE', tax_group = 'vertebrates', all_versions = FALSE))
DefaultAssay(obj) <- 'peaks'
obj <- AddMotifs(obj, genome = BSgenome.Hsapiens.UCSC.hg38, pfm = pfm)

se <- SummarizedExperiment(assays = list(counts = as.matrix(GetAssayData(obj, assay = 'peaks', layer = 'counts'))),
                            rowRanges = granges(obj[['peaks']]))
se <- addGCBias(se, genome = BSgenome.Hsapiens.UCSC.hg38)
motif_ix <- matchMotifs(pfm, se, genome = BSgenome.Hsapiens.UCSC.hg38)

cat('\n--- getBackgroundPeaks() called twice on the IDENTICAL se object, no seed anywhere ---\n')
bg1 <- getBackgroundPeaks(se)
bg2 <- getBackgroundPeaks(se)
cat('dim bg1:', dim(bg1), ' dim bg2:', dim(bg2), '\n')
cat('identical:', identical(bg1, bg2), '\n')
cat('fraction of matrix entries that differ:', mean(bg1 != bg2), '\n')

cat('\n--- Does set.seed() upstream make it reproducible? ---\n')
set.seed(1)
bg3 <- getBackgroundPeaks(se)
set.seed(1)
bg4 <- getBackgroundPeaks(se)
cat('identical with matching set.seed(1) before each call:', identical(bg3, bg4), '\n')
cat('fraction differing bg3 vs bg1 (unseeded):', mean(bg3 != bg1), '\n')

cat('\n--- computeDeviations determinism given the SAME background_peaks input (isolate the two randomness sources) ---\n')
dev_a <- computeDeviations(object = se, annotations = motif_ix, background_peaks = bg1)
dev_b <- computeDeviations(object = se, annotations = motif_ix, background_peaks = bg1)
za <- deviationScores(dev_a); zb <- deviationScores(dev_b)
cat('computeDeviations given IDENTICAL background_peaks -> identical z-scores?', identical(za, zb), '\n')
common_na <- is.na(za) | is.na(zb)
cat('max abs diff (excluding NA positions):', max(abs(za[!common_na] - zb[!common_na])), '\n')

cat('\n--- Full pipeline (bg computed fresh each time) magnitude of z-score drift ---\n')
dev1 <- computeDeviations(object = se, annotations = motif_ix, background_peaks = getBackgroundPeaks(se))
dev2 <- computeDeviations(object = se, annotations = motif_ix, background_peaks = getBackgroundPeaks(se))
z1 <- deviationScores(dev1); z2 <- deviationScores(dev2)
mask <- !is.na(z1) & !is.na(z2)
cat('cells x motifs compared (non-NA both runs):', sum(mask), 'of', length(z1), '\n')
cat('max abs diff (fresh bg each run):', max(abs(z1[mask] - z2[mask])), '\n')
cat('correlation between run1 and run2 z-scores (non-NA overlap):', cor(z1[mask], z2[mask]), '\n')
cat('NA count differs between runs?', sum(is.na(z1)), 'vs', sum(is.na(z2)), '\n')
cat('DONE\n')
