# Input 5 (Stress / multi-part) -- "I pooled 4 samples with CellPlex CMOs but not in
# equal numbers -- one sample is a rare 5% minority. Normalize the HTOs, run HTODemux,
# sanity-check the doublet rate against what I'd expect from loading, tell me if the
# minority sample's tag looks like it failed, and subset to confident singlets. I know
# hashing won't catch same-sample doublets -- what do I still need to run after this?"
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages(library(Seurat))
suppressPackageStartupMessages(library(Matrix))

set.seed(20260919)

hto_df <- read.csv('data/hto_counts_unequal.csv', row.names = 1)
truth <- hto_df[, c('true_class', 'true_sample')]
tag_cols <- c('HTO_A', 'HTO_B', 'HTO_C', 'HTO_D')
hto_mat <- t(as.matrix(hto_df[, tag_cols]))
n_cells <- ncol(hto_mat)

gex_counts <- Matrix(matrix(rpois(400 * n_cells, lambda = 2), nrow = 400, ncol = n_cells),
                      sparse = TRUE)
rownames(gex_counts) <- paste0('GENE_', seq_len(400))
colnames(gex_counts) <- colnames(hto_mat)
obj <- CreateSeuratObject(counts = gex_counts)
obj[['HTO']] <- CreateAssay5Object(counts = hto_mat[, colnames(obj)])
obj <- NormalizeData(obj, assay = 'HTO', normalization.method = 'CLR', margin = 2)
obj <- HTODemux(obj, assay = 'HTO', positive.quantile = 0.99)

cat('=== Global classification ===\n')
print(table(obj$HTO_classification.global))
cat('\n=== Per-sample hash.ID (includes the rare HTO-D minority tag) ===\n')
print(table(obj$hash.ID))

doublet_rate <- mean(obj$HTO_classification.global == 'Doublet')
k <- 4  # number of pooled samples
expected_within_fraction <- 1 / k
cat(sprintf('\nObserved cross-sample doublet rate: %.3f\n', doublet_rate))
cat(sprintf('With k=%d samples, within-sample doublets are expected to be ~1/k = %.3f of all doublets,\n', k, expected_within_fraction))
cat('so hashing-only doublet rate understates the true total doublet rate by roughly that fraction.\n')

# Per-tag singlet counts -- does the minority tag look like a failed antibody or a genuinely rare sample?
singlet_counts_per_tag <- table(obj$hash.ID[obj$HTO_classification.global == 'Singlet'])
cat('\n=== Per-tag singlet counts (check for a failed/near-zero tag) ===\n')
print(singlet_counts_per_tag)
min_tag <- names(which.min(singlet_counts_per_tag))
min_frac <- min(singlet_counts_per_tag) / sum(singlet_counts_per_tag)
cat(sprintf('Smallest tag: %s at %.1f%% of singlets -- present, not near-zero, consistent with a real minority sample rather than a failed antibody (near-zero would be <1%%).\n',
            min_tag, 100 * min_frac))

# Subset to confident singlets
singlets <- subset(obj, subset = HTO_classification.global == 'Singlet')
cat(sprintf('\nSinglets subset: %d cells retained of %d total\n', ncol(singlets), n_cells))

# Accuracy against ground truth
pred_class <- ifelse(obj$HTO_classification.global == 'Singlet', 'singlet',
              ifelse(obj$HTO_classification.global == 'Doublet', 'doublet', 'negative'))
truth_ordered <- truth[colnames(obj), ]
cat(sprintf('\nGlobal class agreement with ground truth: %.3f\n', mean(pred_class == truth_ordered$true_class)))
truth_sample_norm <- gsub('_', '-', truth_ordered$true_sample)
both_singlet <- pred_class == 'singlet' & truth_ordered$true_class == 'singlet'
cat(sprintf('Singlet sample-ID agreement: %.3f\n',
            mean(as.character(obj$hash.ID[both_singlet]) == truth_sample_norm[both_singlet])))

cat('\nNote: this hashing call cannot see within-sample (homotypic) doublets -- two cells from the\n')
cat('same sample share the same tag. Expression-based doublet detection (scDblFinder / Scrublet,\n')
cat('single-cell/doublet-detection) is still required on top of this to catch those.\n')
