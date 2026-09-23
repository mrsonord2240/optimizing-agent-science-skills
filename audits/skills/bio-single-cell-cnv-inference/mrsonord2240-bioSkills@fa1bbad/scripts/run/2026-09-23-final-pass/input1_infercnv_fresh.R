# Purpose: fresh inferCNV regression and malignant-scoring execution.
# Usage: micromamba run -n cnv-audit Rscript input1_infercnv_fresh.R
suppressMessages(library(infercnv))
root <- '/mnt/openscience/audits/bio-single-cell-cnv-inference'
out <- paste0(root, '/2026-09-23-final-pass/run/infercnv_input1')
unlink(out, recursive = TRUE)
dir.create(out, recursive = TRUE)
obj <- CreateInfercnvObject(
  raw_counts_matrix = paste0(root, '/data/counts.matrix'),
  annotations_file = paste0(root, '/data/cell_annotations.txt'), delim = '\t',
  gene_order_file = paste0(root, '/data/gene_ordering.txt'),
  ref_group_names = c('Tcell', 'Myeloid'))
obj <- infercnv::run(obj, cutoff = 0.1, out_dir = out, cluster_by_groups = FALSE,
  analysis_mode = 'subclusters', denoise = TRUE, HMM = TRUE, num_threads = 4)
stopifnot(!file.exists(paste0(out, '/infercnv.observations.txt')))
final <- readRDS(paste0(out, '/run.final.infercnv_obj'))
obs_idx <- unlist(final@observation_grouped_cell_indices)
obs <- final@expr.data[, obs_idx]
scores <- colSums((obs - 1)^2)
truth <- read.table(paste0(root, '/data/ground_truth_clones.txt'), header = TRUE, sep = '\t')
truth <- truth[match(colnames(obs), truth$cell), ]
means <- tapply(scores, truth$group, mean)
print(means)
stopifnot(length(means) >= 2, means[['malignant_cloneA']] > means[['malignant_cloneB']])
cat('PASS: fresh object loaded; the high-CNV malignant clone ranks above the low-CNV malignant clone.\n')
