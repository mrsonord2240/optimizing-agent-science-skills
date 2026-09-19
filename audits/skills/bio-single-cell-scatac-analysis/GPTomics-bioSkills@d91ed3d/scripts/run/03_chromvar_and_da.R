.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({
  library(Signac)
  library(Seurat)
  library(JASPAR2020)
  library(TFBSTools)
  library(motifmatchr)
  library(BSgenome.Hsapiens.UCSC.hg38)
  library(BiocParallel)
})
# chromVAR/motifmatchr default to a multicore BiocParallel backend, which is not supported on Windows
# and hangs silently (observed: an earlier run sat idle at ~122s CPU time for minutes with no output
# and no further CPU use). Force SerialParam, as chromVAR's own vignette recommends on Windows.
register(SerialParam())
flush_cat <- function(...) { cat(...); flush(stdout()) }

data_dir <- 'F:/OpenScience/audits/bio-single-cell-scatac-analysis/data'
obj <- readRDS(file.path(data_dir, 'obj_qc.rds'))
cat('Loaded object:', ncol(obj), 'cells x', nrow(obj), 'peaks\n')

# ---- chromVAR motif deviations, exactly the skill's documented pattern ----
pfm <- getMatrixSet(JASPAR2020, opts = list(collection = 'CORE', tax_group = 'vertebrates', all_versions = FALSE))
cat('PFMs fetched:', length(pfm), '\n')

DefaultAssay(obj) <- 'peaks'
obj <- AddMotifs(obj, genome = BSgenome.Hsapiens.UCSC.hg38, pfm = pfm)

# FINDING: SKILL.md's documented `RunChromVAR(obj, genome = ...)` call throws
# `could not find function "RunChromVAR"` on the installed Signac 1.17.1 -- confirmed against
# Signac's own NEWS.md: "Removed RunChromVAR() and AddChromatinModule() due to the chromVAR package
# being unavailable in Bioconductor 3.23." This is not an environment quirk: the function is gone from
# the CRAN release the skill's own Version Compatibility note says to target (1.13+). Falling back to
# chromVAR's own lower-level API (what RunChromVAR used to wrap) to still validate the skill's stated
# methodology (GC-matched background, z-score ranking).
suppressPackageStartupMessages(library(chromVAR))
suppressPackageStartupMessages(library(SummarizedExperiment))
cat('chromVAR package version (fallback path):', as.character(packageVersion('chromVAR')), '\n')

peak_counts_mat <- GetAssayData(obj, assay = 'peaks', layer = 'counts')
peak_gr_full <- granges(obj[['peaks']])
se <- SummarizedExperiment(assays = list(counts = as.matrix(peak_counts_mat)), rowRanges = peak_gr_full)
se <- addGCBias(se, genome = BSgenome.Hsapiens.UCSC.hg38)
motif_ix <- motifmatchr::matchMotifs(pfm, se, genome = BSgenome.Hsapiens.UCSC.hg38)
bg_peaks <- getBackgroundPeaks(se)  # GC- and accessibility-matched background, as the skill specifies
dev <- computeDeviations(object = se, annotations = motif_ix, background_peaks = bg_peaks)
cat('chromVAR deviations object dims (motifs x cells):', dim(dev), '\n')

z_scores <- deviationScores(dev)  # background-normalized; SKILL.md: "Use z-scores... raw deviations are not comparable"
chromvar_assay <- CreateAssayObject(data = z_scores)
obj[['chromvar']] <- chromvar_assay
cat('chromVAR assay dims:', dim(obj[['chromvar']]), '\n')

DefaultAssay(obj) <- 'chromvar'
diff_motifs <- FindMarkers(obj, ident.1 = '0', ident.2 = '1',
                            group.by = 'seurat_clusters',
                            mean.fxn = rowMeans, fc.name = 'avg_diff')
cat('Differential motifs found:', nrow(diff_motifs), '\n')
cat('Top 5 by |avg_diff|, ranked by z-score difference (as the skill specifies, not raw deviation):\n')
diff_motifs <- diff_motifs[order(-abs(diff_motifs$avg_diff)), ]
print(head(diff_motifs, 5))

# Resolve top motif IDs -> TF names for a sanity check
top_ids <- rownames(head(diff_motifs, 5))
motif_names <- sapply(pfm[top_ids], function(x) name(x))
cat('Top motif TF identities:\n')
print(motif_names)

# ---- Differential accessibility on the peaks assay, controlling for depth (skill's documented pattern) ----
DefaultAssay(obj) <- 'peaks'
da <- FindMarkers(obj, ident.1 = '0', ident.2 = '1', group.by = 'seurat_clusters',
                   test.use = 'LR', latent.vars = 'nCount_peaks')
cat('DA peaks found (p_val_adj<0.05):', sum(da$p_val_adj < 0.05), 'of', nrow(da), 'tested\n')
da_sig <- da[da$p_val_adj < 0.05, ]
da_sig <- da_sig[order(da_sig$p_val_adj), ]
print(head(da_sig, 10))

# Cross-check: do the significant DA peaks fall in the marker gene windows we built the synthetic signal from?
gene_windows <- readRDS(file.path(data_dir, 'gene_windows.rds'))
peak_gr <- StringToGRanges(rownames(da_sig), sep = c(':', '-'))
ov <- findOverlaps(peak_gr, gene_windows)
cat('Of', length(peak_gr), 'significant DA peaks,', length(unique(queryHits(ov))), 'overlap a known marker-gene window (expected: mostly CD3D/MS4A1)\n')
if (length(ov) > 0) {
  print(table(names(gene_windows)[subjectHits(ov)]))
}

saveRDS(obj, file.path(data_dir, 'obj_chromvar.rds'))
cat('STAGE 3 DONE\n')
