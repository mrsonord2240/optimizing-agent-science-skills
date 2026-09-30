#!/bin/bash
# Audit run: T1 - documented CLI path of scripts/cicero_workflow.R on readMM output, plus class diagnosis.
source /mnt/openscience/audit-envs/bio-atac-seq-co-accessibility/tools/env.sh
W=$CO/work/audit_cli; mkdir -p $W; cd $W
cp $CO/work/patched/gencode_v29_protein_coding_tss.bed .
I=$CO/work/input
echo "== CLI as documented (Rscript scripts/cicero_workflow.R m.mtx peak_meta.tsv cell_meta.tsv)"
micromamba run -n bio-atac-seq-co-accessibility Rscript $SKILL/scripts/cicero_workflow.R $I/peak_matrix.mtx $I/peak_metadata.tsv $I/cell_metadata.tsv
echo "CLI_EXIT=$?"
echo "== diagnosis"
micromamba run -n bio-atac-seq-co-accessibility Rscript -e '
suppressPackageStartupMessages({library(Matrix); library(monocle3)})
I <- Sys.getenv("CO"); I <- file.path(I, "work/input")
m <- Matrix::readMM(file.path(I, "peak_matrix.mtx"))
cat("readMM class:", class(m), " dimnames NULL:", is.null(dimnames(m)), "\n")
pm <- read.delim(file.path(I, "peak_metadata.tsv"), row.names=1); cm <- read.delim(file.path(I, "cell_metadata.tsv"), row.names=1)
r <- try(new_cell_data_set(m, cell_metadata=cm, gene_metadata=pm), silent=TRUE)
cat("new_cell_data_set(readMM output):", if (inherits(r, "try-error")) trimws(as.character(r)) else "OK", "\n")
m2 <- as(m, "CsparseMatrix"); dimnames(m2) <- list(rownames(pm), rownames(cm))
r2 <- try(new_cell_data_set(m2, cell_metadata=cm, gene_metadata=pm), silent=TRUE)
cat("diagnostic only (CsparseMatrix + dimnames added by caller):", if (inherits(r2, "try-error")) trimws(as.character(r2)) else sprintf("OK %d x %d", nrow(r2), ncol(r2)), "\n")
' 2>&1 | grep -v -E "lme4|Matrix ABI|check_dep|Please re-install"
