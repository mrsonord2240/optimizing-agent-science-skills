.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
library(DropletUtils)
library(Matrix)

# Independent synthetic CITE-seq data (own seed, own shape) written as REAL 10x-format
# directories so examples/cite_seq_analysis.R can be run completely unmodified
# (Read10X against raw_feature_bc_matrix/ and filtered_feature_bc_matrix/), which is a
# stronger regression test than reusing the audit's .rds object.
set.seed(9001)
n_genes <- 3000
n_adt <- 12
n_per_type <- 80  # 240 real cells
n_empty <- 1200

gene_names <- c(paste0("MT-", 1:5), paste0("GENE", 1:(n_genes - 5)))
markers <- list(Tcell = c("GENE1","GENE2"), Bcell = c("GENE8","GENE9"), Mono = c("GENE15","GENE16"))
adt_names <- c("CD3","CD4","CD8","CD14","CD19","CD16","CD56","CD27",
               "PD1","CTLA4","Isotype-Mouse-IgG1","Isotype-Rat-IgG2b")
adt_markers <- list(Tcell = c("CD3","CD4"), Bcell = c("CD19","CD27"), Mono = c("CD14","CD16"))

make_cells <- function(celltype, n) {
  rna <- matrix(rpois(n_genes * n, lambda = 0.3), nrow = n_genes, ncol = n)
  rownames(rna) <- gene_names
  for (g in markers[[celltype]]) rna[g, ] <- rpois(n, lambda = 12)
  adt <- matrix(rpois(n_adt * n, lambda = 6), nrow = n_adt, ncol = n)
  rownames(adt) <- adt_names
  for (a in adt_markers[[celltype]]) adt[a, ] <- adt[a, ] + rpois(n, lambda = 100)
  list(rna = rna, adt = adt)
}

tc <- make_cells("Tcell", n_per_type)
bc <- make_cells("Bcell", n_per_type)
mo <- make_cells("Mono", n_per_type)
rna_cells <- cbind(tc$rna, bc$rna, mo$rna)
adt_cells <- cbind(tc$adt, bc$adt, mo$adt)
cell_bc <- paste0("CELL-", seq_len(ncol(rna_cells)), "-1")
colnames(rna_cells) <- cell_bc; colnames(adt_cells) <- cell_bc
truth <- rep(c("Tcell","Bcell","Mono"), each = n_per_type)

rna_empty <- matrix(rpois(n_genes * n_empty, lambda = 0.03), nrow = n_genes, ncol = n_empty)
rownames(rna_empty) <- gene_names
adt_empty <- matrix(rpois(n_adt * n_empty, lambda = 2), nrow = n_adt, ncol = n_empty)
rownames(adt_empty) <- adt_names
empty_bc <- paste0("EMPTY-", seq_len(n_empty), "-1")
colnames(rna_empty) <- empty_bc; colnames(adt_empty) <- empty_bc

# 10x write10xCounts wants ONE matrix with gene.type per feature. Combine RNA+ADT rows for both
# filtered and raw and tag feature type so Read10X returns a list with $`Gene Expression`
# and $`Antibody Capture`, matching examples/cite_seq_analysis.R's expectations.
combo_filtered <- rbind(rna_cells, adt_cells)
combo_raw <- rbind(rna_empty, adt_empty)  # raw = unfiltered (empties only here is fine: DSB only needs empties from raw)
# but Read10X needs a self-consistent raw matrix that also usually contains the cells;
# include cells + empties in raw, as real 10x raw matrices do
combo_raw_full <- cbind(rbind(rna_cells, adt_cells), rbind(rna_empty, adt_empty))

feature_type <- c(rep("Gene Expression", n_genes), rep("Antibody Capture", n_adt))

dir.create("filtered_feature_bc_matrix", showWarnings = FALSE)
dir.create("raw_feature_bc_matrix", showWarnings = FALSE)

write10xCounts("filtered_feature_bc_matrix", as(combo_filtered, "CsparseMatrix"),
                gene.id = rownames(combo_filtered), gene.symbol = rownames(combo_filtered),
                gene.type = feature_type, barcodes = colnames(combo_filtered),
                type = "sparse", overwrite = TRUE, version = "3")
write10xCounts("raw_feature_bc_matrix", as(combo_raw_full, "CsparseMatrix"),
                gene.id = rownames(combo_raw_full), gene.symbol = rownames(combo_raw_full),
                gene.type = feature_type, barcodes = colnames(combo_raw_full),
                type = "sparse", overwrite = TRUE, version = "3")

saveRDS(truth, "truth.rds")
cat("Wrote 10x-format dirs:", ncol(combo_filtered), "filtered barcodes,",
    ncol(combo_raw_full), "raw barcodes\n")
