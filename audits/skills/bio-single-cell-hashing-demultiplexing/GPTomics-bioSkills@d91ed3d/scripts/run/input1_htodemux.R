# Input 1 (Canonical) -- "I have hashed cells pooled from 4 samples with CITE-seq HTO
# antibody tags. Assign each cell to its sample of origin and flag cross-sample doublets."
# Follows the Skill's examples/htodemux_seurat.R pattern verbatim (CLR margin=2,
# HTODemux positive.quantile=0.99), applied to synthetic data with known ground truth.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages(library(Seurat))
suppressPackageStartupMessages(library(Matrix))

set.seed(20260919)

hto_df <- read.csv('data/hto_counts_4tag.csv', row.names = 1)
truth <- hto_df[, c('true_class', 'true_sample')]
hto_mat <- t(as.matrix(hto_df[, c('HTO_A', 'HTO_B', 'HTO_C', 'HTO_D')]))

n_cells <- ncol(hto_mat)
n_genes <- 500
# Synthetic GEX counts -- not derived from HTO signal, just plausible sparse Poisson counts
gex_counts <- matrix(rpois(n_genes * n_cells, lambda = 2), nrow = n_genes, ncol = n_cells)
rownames(gex_counts) <- paste0('GENE_', seq_len(n_genes))
colnames(gex_counts) <- colnames(hto_mat)
gex_counts <- Matrix(gex_counts, sparse = TRUE)

obj <- CreateSeuratObject(counts = gex_counts)
obj[['HTO']] <- CreateAssay5Object(counts = hto_mat[, colnames(obj)])

obj <- NormalizeData(obj, assay = 'HTO', normalization.method = 'CLR', margin = 2)
obj <- HTODemux(obj, assay = 'HTO', positive.quantile = 0.99)

global_counts <- table(obj$HTO_classification.global)
sample_counts <- table(obj$hash.ID)
doublet_rate <- global_counts['Doublet'] / sum(global_counts)

cat('=== HTODemux global classification ===\n')
print(global_counts)
cat('\n=== HTODemux per-sample hash.ID ===\n')
print(sample_counts)
cat(sprintf('\nCross-sample doublet rate: %.3f\n', doublet_rate))

# Accuracy against ground truth
pred_class <- ifelse(obj$HTO_classification.global == 'Singlet', 'singlet',
              ifelse(obj$HTO_classification.global == 'Doublet', 'doublet', 'negative'))
truth_ordered <- truth[colnames(obj), ]
agree <- pred_class == truth_ordered$true_class
cat(sprintf('\nGlobal class agreement with ground truth: %d / %d = %.3f\n',
            sum(agree), length(agree), mean(agree)))

# Singlet sample-assignment accuracy (only where both truth and HTODemux say singlet)
# Note: Seurat's CreateAssay5Object sanitizes feature names, replacing '_' with '-'
# (HTO_A -> HTO-A); normalize both sides before comparing.
both_singlet <- pred_class == 'singlet' & truth_ordered$true_class == 'singlet'
truth_sample_norm <- gsub('_', '-', truth_ordered$true_sample)
sample_agree <- as.character(obj$hash.ID[both_singlet]) == truth_sample_norm[both_singlet]
cat(sprintf('Singlet sample-ID agreement (both-singlet subset): %d / %d = %.3f\n',
            sum(sample_agree), length(sample_agree), mean(sample_agree)))

# Confusion of predicted global class vs ground truth
cat('\n=== Confusion: predicted global class (rows) vs ground truth (cols) ===\n')
print(table(pred_class, truth_ordered$true_class))
