# Synthetic CITE-seq data generator for the multimodal-integration audit.
# Creates a raw (unfiltered, includes empty droplets) and filtered (called cells)
# 10x-style RNA + ADT count matrix with 3 known cell populations (T, B, Mono)
# so DSB denoising and WNN clustering have real signal to recover.
set.seed(42)

n_genes <- 600
n_adt <- 15
n_cells_per_type <- 100  # 300 real cells total
n_empty <- 2000

gene_names <- c(paste0("MT-", 1:6), paste0("GENE", 1:(n_genes - 6)))
# marker genes used to drive per-population RNA signal
markers <- list(Tcell = c("GENE1","GENE2","GENE3"),
                Bcell = c("GENE10","GENE11","GENE12"),
                Mono  = c("GENE20","GENE21","GENE22"))

adt_names <- c("CD3","CD4","CD8","CD14","CD19","CD16","CD56","CD25","CD27",
               "CD45RA","CD45RO","PD1","CTLA4",
               "Isotype-Mouse-IgG1","Isotype-Rat-IgG2b")
adt_markers <- list(Tcell = c("CD3","CD4","CD8"),
                     Bcell = c("CD19","CD27"),
                     Mono  = c("CD14","CD16"))

make_cells <- function(celltype, n) {
  rna <- matrix(rpois(n_genes * n, lambda = 0.5), nrow = n_genes, ncol = n)
  rownames(rna) <- gene_names
  for (g in markers[[celltype]]) rna[g, ] <- rpois(n, lambda = 15)
  adt <- matrix(rpois(n_adt * n, lambda = 8), nrow = n_adt, ncol = n)  # ambient + intrinsic background
  rownames(adt) <- adt_names
  for (a in adt_markers[[celltype]]) adt[a, ] <- adt[a, ] + rpois(n, lambda = 120)
  list(rna = rna, adt = adt)
}

tc <- make_cells("Tcell", n_cells_per_type)
bc <- make_cells("Bcell", n_cells_per_type)
mo <- make_cells("Mono", n_cells_per_type)

rna_cells <- cbind(tc$rna, bc$rna, mo$rna)
adt_cells <- cbind(tc$adt, bc$adt, mo$adt)
cell_barcodes <- paste0("CELL-", seq_len(ncol(rna_cells)))
colnames(rna_cells) <- cell_barcodes
colnames(adt_cells) <- cell_barcodes
truth <- rep(c("Tcell","Bcell","Mono"), each = n_cells_per_type)
names(truth) <- cell_barcodes

# empty droplets: ambient-only, low counts, no cell-intrinsic marker elevation
rna_empty <- matrix(rpois(n_genes * n_empty, lambda = 0.05), nrow = n_genes, ncol = n_empty)
rownames(rna_empty) <- gene_names
adt_empty <- matrix(rpois(n_adt * n_empty, lambda = 3), nrow = n_adt, ncol = n_empty)  # ambient antibody
rownames(adt_empty) <- adt_names
empty_barcodes <- paste0("EMPTY-", seq_len(n_empty))
colnames(rna_empty) <- empty_barcodes
colnames(adt_empty) <- empty_barcodes

rna_raw <- cbind(rna_cells, rna_empty)
adt_raw <- cbind(adt_cells, adt_empty)

dir.create("data", showWarnings = FALSE)
saveRDS(list(rna_cells = rna_cells, adt_cells = adt_cells,
             rna_raw = rna_raw, adt_raw = adt_raw, truth = truth),
        "data/synthetic_cite_seq.rds")
cat("Synthetic CITE-seq data written: ", ncol(rna_cells), "cells,",
    ncol(rna_empty), "empty droplets,", n_genes, "genes,", n_adt, "ADT.\n")
