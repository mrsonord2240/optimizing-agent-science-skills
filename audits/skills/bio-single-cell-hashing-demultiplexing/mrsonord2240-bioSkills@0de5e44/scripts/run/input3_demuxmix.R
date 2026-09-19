# Input 3 (Edge/boundary) -- "My HTODemux call gives a huge Negative pile from weak
# antibody staining. Which method should I use to rescue it, and how do I run it?"
# The Skill recommends demuxmix for uneven staining / weak signal. Run demuxmix on the
# synthetic weak-staining dataset (heavy ambient background, 3 tags) and compare against
# a naive HTODemux-style quantile call on the same data to show the claimed rescue effect.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages(library(demuxmix))
suppressPackageStartupMessages(library(Seurat))
suppressPackageStartupMessages(library(Matrix))

set.seed(20260919)

hto_df <- read.csv('data/hto_counts_weak.csv', row.names = 1)
truth <- hto_df[, c('true_class', 'true_sample')]
tag_cols <- c('HTO_X', 'HTO_Y', 'HTO_Z')
hto_mat <- t(as.matrix(hto_df[, tag_cols]))
n_cells <- ncol(hto_mat)

# Synthetic per-cell detected-gene count (demuxmix's regression covariate `rna`);
# not derived from the HTO signal.
rna_counts <- rpois(n_cells, lambda = 150)

# --- Baseline: HTODemux-style quantile call on the same weak-staining data ---
gex_counts <- Matrix(matrix(rpois(300 * n_cells, lambda = 2), nrow = 300, ncol = n_cells),
                      sparse = TRUE)
rownames(gex_counts) <- paste0('GENE_', seq_len(300))
colnames(gex_counts) <- colnames(hto_mat)
obj <- CreateSeuratObject(counts = gex_counts)
obj[['HTO']] <- CreateAssay5Object(counts = hto_mat[, colnames(obj)])
obj <- NormalizeData(obj, assay = 'HTO', normalization.method = 'CLR', margin = 2)
obj <- HTODemux(obj, assay = 'HTO', positive.quantile = 0.99)
cat('=== Baseline HTODemux on weak-staining data ===\n')
print(table(obj$HTO_classification.global))

# --- demuxmix rescue ---
dmm <- demuxmix(as.matrix(hto_mat), rna = rna_counts)
classified <- dmmClassify(dmm)
cat('\n=== demuxmix classification ===\n')
print(table(classified$HTO))

# Map demuxmix HTO calls to global class (singlet/doublet/negative) for comparison
demux_global <- ifelse(classified$HTO == 'negative', 'negative',
                 ifelse(grepl(',', classified$HTO), 'doublet', 'singlet'))
cat('\n=== demuxmix global (singlet/doublet/negative) ===\n')
print(table(demux_global))

htodemux_global <- tolower(as.character(obj$HTO_classification.global))
truth_ordered <- truth[colnames(obj), ]

cat(sprintf('\nBaseline HTODemux agreement with truth: %.3f\n',
            mean(htodemux_global == truth_ordered$true_class)))
cat(sprintf('demuxmix agreement with truth:          %.3f\n',
            mean(demux_global == truth_ordered$true_class)))

cat(sprintf('\nBaseline HTODemux Negative fraction: %.3f\n', mean(htodemux_global == 'negative')))
cat(sprintf('demuxmix Negative fraction:          %.3f\n', mean(demux_global == 'negative')))
cat(sprintf('True negative fraction:              %.3f\n', mean(truth_ordered$true_class == 'negative')))
