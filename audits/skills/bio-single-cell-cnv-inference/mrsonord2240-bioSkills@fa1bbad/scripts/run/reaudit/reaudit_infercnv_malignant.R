# RE-AUDIT (2026-09-19): independent fresh run to verify the fixed
# malignant-calling code path (readRDS('run.final.infercnv_obj') instead of
# the removed infercnv.observations.txt). Uses the audit's original
# 3-chromosome synthetic panel (data/), a FRESH inferCNV run into a new
# out_dir (not reusing the original auditor's or fixer's run outputs).
suppressMessages(library(infercnv))

setwd("/mnt/openscience/audits/bio-single-cell-cnv-inference")

infercnv_obj <- CreateInfercnvObject(
    raw_counts_matrix = "data/counts.matrix",
    annotations_file = "data/cell_annotations.txt",
    delim = "\t",
    gene_order_file = "data/gene_ordering.txt",
    ref_group_names = c("Tcell", "Myeloid"))

infercnv_obj <- infercnv::run(
    infercnv_obj,
    cutoff = 0.1,
    out_dir = "run/reaudit/infercnv_out_reaudit",
    cluster_by_groups = FALSE,
    analysis_mode = "subclusters",
    denoise = TRUE,
    HMM = TRUE,
    num_threads = 4)

# --- exact malignant-calling code as shipped in examples/infercnv_malignant_calling.R ---
old_file <- "run/reaudit/infercnv_out_reaudit/infercnv.observations.txt"
cat("infercnv.observations.txt exists (old path, should be FALSE under 1.22 HMM/subclusters):",
    file.exists(old_file), "\n")

infercnv_obj_final <- readRDS("run/reaudit/infercnv_out_reaudit/run.final.infercnv_obj")
obs_idx <- unlist(infercnv_obj_final@observation_grouped_cell_indices)
obs <- infercnv_obj_final@expr.data[, obs_idx]
cnv_score <- colSums((obs - 1)^2)
malignant <- cnv_score > quantile(cnv_score, 0.5)

# Ground truth comparison
truth <- read.table("data/ground_truth_clones.txt", header = TRUE, sep = "\t")
rownames(truth) <- truth$cell
truth_sub <- truth[colnames(obs), ]

cat("\n--- cnv_score by true group ---\n")
print(tapply(cnv_score, truth_sub$group, mean))

cat("\n--- malignant call vs truth (table) ---\n")
print(table(called_malignant = malignant, true_group = truth_sub$group))

cat("\nDONE: reaudit inferCNV malignant-calling verification complete\n")
