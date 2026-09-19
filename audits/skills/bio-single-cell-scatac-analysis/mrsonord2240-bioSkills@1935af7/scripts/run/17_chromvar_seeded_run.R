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

# Usage: rs.sh 17_chromvar_seeded_run.R <run_index> <seeded|unseeded>
args <- commandArgs(trailingOnly = TRUE)
run_idx <- args[1]
mode <- args[2]  # "seeded" or "unseeded"

data_dir <- 'F:/OpenScience/audits/bio-single-cell-scatac-analysis/data/reaudit4_20260919'
obj <- readRDS(file.path(data_dir, 'obj_qc.rds'))
cat('[run', run_idx, mode, '] Loaded object:', ncol(obj), 'cells x', nrow(obj), 'peaks\n')

pfm <- getMatrixSet(JASPAR2020, opts = list(collection = 'CORE', tax_group = 'vertebrates', all_versions = FALSE))
cat('[run', run_idx, mode, '] PFMs fetched:', length(pfm), '\n')

DefaultAssay(obj) <- 'peaks'
obj <- AddMotifs(obj, genome = BSgenome.Hsapiens.UCSC.hg38, pfm = pfm)

# ---- EXACT block as it appears in the fixed SKILL.md (commit 4c65703), chromVAR Motif Deviations ----
se <- SummarizedExperiment(assays = list(counts = as.matrix(GetAssayData(obj, assay = 'peaks', layer = 'counts'))),
                            rowRanges = granges(obj[['peaks']]))
se <- addGCBias(se, genome = BSgenome.Hsapiens.UCSC.hg38)
motif_ix <- matchMotifs(pfm, se, genome = BSgenome.Hsapiens.UCSC.hg38)
if (mode == 'seeded') {
  set.seed(1)                                        # exactly as documented in SKILL.md
}
bg_peaks <- getBackgroundPeaks(se)
dev <- computeDeviations(object = se, annotations = motif_ix, background_peaks = bg_peaks)
z <- deviationScores(dev)
obj[['chromvar']] <- CreateAssayObject(data = z)
DefaultAssay(obj) <- 'chromvar'
diff_motifs <- FindMarkers(obj, ident.1 = 'Tcell', ident.2 = 'Bcell', group.by = 'cell_type',
                            mean.fxn = rowMeans, fc.name = 'avg_diff')
diff_motifs <- diff_motifs[order(diff_motifs$p_val_adj), ]

out_dir <- file.path(data_dir, 'chromvar_runs')
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)
saveRDS(list(bg_peaks = bg_peaks, z = z, diff_motifs = diff_motifs),
        file.path(out_dir, paste0(mode, '_run', run_idx, '.rds')))

n_sig <- sum(diff_motifs$p_val_adj < 0.05, na.rm = TRUE)
top10 <- rownames(head(diff_motifs, 10))
cat('[run', run_idx, mode, '] dims (motifs x cells):', dim(dev), '\n')
cat('[run', run_idx, mode, '] Significant motifs (p_val_adj<0.05):', n_sig, 'of', nrow(diff_motifs), '\n')
cat('[run', run_idx, mode, '] Top10 motif IDs:', paste(top10, collapse = ' '), '\n')
cat('[run', run_idx, mode, '] DONE\n')
