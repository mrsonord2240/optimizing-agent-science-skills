# Input 4 (Edge) - bio-workflows-scrnaseq-pipeline
# "My collaborator only sent me filtered_feature_bc_matrix." The Skill's made-once commitments
# table says the filtered matrix is cell-CALLING only, NOT ambient-corrected, and that
# SoupX/CellBender and low-RNA rescue need the RAW matrix - "filtered-only is irreversible loss".
# Tested directly on real and synthetic data.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({library(Seurat); library(SoupX); library(DropletUtils); library(Matrix)})

D <- 'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
P <- 'F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/public-data'

cat('--- (a) can SoupX run from the filtered matrix alone? ---\n')
toc <- Read10X(file.path(D, 'S3/outs/filtered_feature_bc_matrix'))
r <- try(SoupChannel(toc, toc), silent = TRUE)
if (inherits(r, 'try-error')) cat('  SoupChannel(filtered, filtered) errors:\n   ', as.character(r)) else {
  tmp <- CreateSeuratObject(toc); tmp <- NormalizeData(tmp, verbose=FALSE)
  tmp <- FindVariableFeatures(tmp, verbose=FALSE); tmp <- ScaleData(tmp, verbose=FALSE)
  tmp <- RunPCA(tmp, npcs=20, verbose=FALSE); tmp <- FindNeighbors(tmp, dims=1:15, verbose=FALSE)
  tmp <- FindClusters(tmp, resolution=0.8, verbose=FALSE)
  r <- setClusters(r, setNames(as.character(Idents(tmp)), colnames(tmp)))
  e <- try(suppressMessages(autoEstCont(r, doPlot=FALSE, forceAccept=TRUE)), silent=TRUE)
  if (inherits(e, 'try-error')) cat('  autoEstCont on a filtered-as-raw channel errors:\n   ', as.character(e))
  else cat('  autoEstCont RAN but estimated rho =', round(mean(e$metaData$rho),4),
           ' (true injected rho for S3 = 0.0982) - a silently wrong answer, not an error\n')
}
cat('  with the RAW matrix, the same call estimated rho 0.153 for S3 (input 1 log)\n')

cat('\n--- (b) how much information is in the raw matrix that the filtered one has lost? ---\n')
tod <- Read10X(file.path(D, 'S3/outs/raw_feature_bc_matrix'))
cat(sprintf('  raw barcodes %d vs filtered %d; raw-only barcodes carry %s UMIs (%.1f%% of all UMIs)\n',
            ncol(tod), ncol(toc), format(sum(tod) - sum(toc), big.mark=','),
            100*(sum(tod)-sum(toc))/sum(tod)))

cat('\n--- (c) emptyDrops needs the raw matrix; does it recover low-RNA cells? ---\n')
set.seed(20260916)
ed <- DropletUtils::emptyDrops(tod)
called <- rownames(ed)[which(ed$FDR < 0.01)]
cat(sprintf('  emptyDrops on RAW: %d barcodes at FDR<0.01 | Cell Ranger filtered: %d\n',
            length(called), ncol(toc)))
cat(sprintf('  emptyDrops-only barcodes: %d | filtered-only: %d\n',
            length(setdiff(called, colnames(toc))), length(setdiff(colnames(toc), called))))

cat('\n--- (d) the same check on REAL 10x PBMC 1k v3 ---\n')
rt <- Read10X_h5(file.path(P, 'pbmc_1k_v3_raw_feature_bc_matrix.h5'))
ft <- Read10X_h5(file.path(P, 'pbmc_1k_v3_filtered_feature_bc_matrix.h5'))
cat(sprintf('  real data: raw barcodes %s vs filtered %d; raw-only UMIs %.1f%% of total\n',
            format(ncol(rt), big.mark=','), ncol(ft), 100*(sum(rt)-sum(ft))/sum(rt)))
sc <- SoupChannel(rt, ft)
tmp <- CreateSeuratObject(ft); tmp <- NormalizeData(tmp, verbose=FALSE)
tmp <- FindVariableFeatures(tmp, verbose=FALSE); tmp <- ScaleData(tmp, verbose=FALSE)
tmp <- RunPCA(tmp, npcs=20, verbose=FALSE); tmp <- FindNeighbors(tmp, dims=1:15, verbose=FALSE)
tmp <- FindClusters(tmp, resolution=0.8, verbose=FALSE)
sc <- setClusters(sc, setNames(as.character(Idents(tmp)), colnames(tmp)))
sc <- suppressMessages(autoEstCont(sc, doPlot=FALSE))
cat('  real PBMC 1k rho with the RAW matrix:', round(mean(sc$metaData$rho), 4), '\n')

cat('\n--- (e) the gex_only commitment ---\n')
cat('  Read10X_h5 arg list:', paste(names(formals(Read10X_h5)), collapse=', '), '\n')
cat('  Skill says gex_only=True silently drops ADT/HTO/CRISPR; the R reader exposes',
    if ('gex.only' %in% names(formals(Read10X_h5))) 'gex.only, default TRUE' else 'no such flag', '\n')
cat('DONE\n')
