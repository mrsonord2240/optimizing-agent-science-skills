.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({
  library(Signac); library(Seurat); library(JASPAR2020); library(TFBSTools)
  library(motifmatchr); library(BSgenome.Hsapiens.UCSC.hg38); library(BiocParallel)
  library(chromVAR); library(SummarizedExperiment)
})
register(SerialParam())

skill_txt <- paste(readLines('F:/OpenScience/wt/sc-atac/single-cell/scatac-analysis/SKILL.md'), collapse = '\n')
cat('SKILL.md contains set.seed anywhere:', grepl('set\\.seed', skill_txt), '\n')

data_dir <- 'F:/OpenScience/audits/bio-single-cell-scatac-analysis/data/reaudit_v2_20260919'
obj <- readRDS(file.path(data_dir, 'obj_qc.rds'))
pfm <- getMatrixSet(JASPAR2020, opts = list(collection = 'CORE', tax_group = 'vertebrates', all_versions = FALSE))
DefaultAssay(obj) <- 'peaks'
obj <- AddMotifs(obj, genome = BSgenome.Hsapiens.UCSC.hg38, pfm = pfm)

run_full <- function(obj, tag) {
  se <- SummarizedExperiment(assays = list(counts = as.matrix(GetAssayData(obj, assay = 'peaks', layer = 'counts'))),
                              rowRanges = granges(obj[['peaks']]))
  se <- addGCBias(se, genome = BSgenome.Hsapiens.UCSC.hg38)
  motif_ix <- matchMotifs(pfm, se, genome = BSgenome.Hsapiens.UCSC.hg38)
  bg_peaks <- getBackgroundPeaks(se)
  dev <- computeDeviations(object = se, annotations = motif_ix, background_peaks = bg_peaks)
  z <- deviationScores(dev)
  o2 <- obj
  o2[[paste0('chromvar_', tag)]] <- CreateAssayObject(data = z)
  DefaultAssay(o2) <- paste0('chromvar_', tag)
  dm <- FindMarkers(o2, ident.1 = 'Tcell', ident.2 = 'Bcell', group.by = 'cell_type',
                     mean.fxn = rowMeans, fc.name = 'avg_diff')
  dm <- dm[order(dm$p_val_adj), ]
  top10 <- rownames(head(dm, 10))
  list(dm = dm, top10 = top10, n_sig = sum(dm$p_val_adj < 0.05, na.rm = TRUE))
}

r1 <- run_full(obj, 'r1')
r2 <- run_full(obj, 'r2')
r3 <- run_full(obj, 'r3')

cat('\nRun1 top10 motif IDs:\n'); print(r1$top10)
cat('Run2 top10 motif IDs:\n'); print(r2$top10)
cat('Run3 top10 motif IDs:\n'); print(r3$top10)

cat('\nOverlap top10 run1 vs run2:', length(intersect(r1$top10, r2$top10)), '/10\n')
cat('Overlap top10 run1 vs run3:', length(intersect(r1$top10, r3$top10)), '/10\n')
cat('Overlap top10 run2 vs run3:', length(intersect(r2$top10, r3$top10)), '/10\n')

cat('\nTop1 motif run1/run2/run3:', rownames(head(r1$dm,1)), '/', rownames(head(r2$dm,1)), '/', rownames(head(r3$dm,1)), '\n')
top1_names <- sapply(pfm[c(rownames(head(r1$dm,1)), rownames(head(r2$dm,1)), rownames(head(r3$dm,1)))], name)
cat('Top1 TF name run1/run2/run3:', paste(top1_names, collapse=' / '), '\n')

cat('\nN significant (p_adj<0.05) run1/run2/run3:', r1$n_sig, r2$n_sig, r3$n_sig, '\n')
cat('DONE\n')
