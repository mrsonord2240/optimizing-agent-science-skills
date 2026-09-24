# Input 1 (Canonical) - bio-workflows-scrnaseq-pipeline
# The whole point of a workflow skill: 8-sample Cell Ranger output -> annotated cell types,
# honouring the ordering rules the Skill owns (ambient -> doublets -> per-sample QC -> merge ->
# integrate -> cluster -> annotate). Scored end to end against the SYNTHETIC ground truth.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({
  library(Seurat); library(scDblFinder); library(SingleCellExperiment); library(SoupX)
  library(harmony); library(dplyr); library(Matrix)
})
options(future.globals.maxSize = 4 * 1024^3)
cat('Seurat', as.character(packageVersion('Seurat')), '| scDblFinder',
    as.character(packageVersion('scDblFinder')), '| SoupX', as.character(packageVersion('SoupX')),
    '| harmony', as.character(packageVersion('harmony')), '\n')

D <- 'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
OUT <- 'F:/OpenScience/audits/bio-workflows-scrnaseq-pipeline'
tc <- read.csv(file.path(D, 'truth_cells.csv'))
tc$true_doublet <- tc$true_doublet %in% c('True','TRUE',TRUE)
tc$true_low_quality <- tc$true_low_quality %in% c('True','TRUE',TRUE)
rownames(tc) <- tc$cell_id
ss <- read.csv(file.path(D, 'sample_sheet.csv')); rownames(ss) <- ss$sample
ari <- function(x,y){t<-table(x,y);n<-sum(t);s<-sum(choose(t,2));a<-sum(choose(rowSums(t),2))
  b<-sum(choose(colSums(t),2));e<-a*b/choose(n,2);(s-e)/((a+b)/2-e)}
set.seed(20260916)

## ---- Stage 0-2: per sample, ambient -> QC -> doublets, BEFORE any merge ----
objs <- list(); audit <- list()
for (s in paste0('S', 1:8)) {
  tod <- Read10X(file.path(D, s, 'outs/raw_feature_bc_matrix'))
  toc <- Read10X(file.path(D, s, 'outs/filtered_feature_bc_matrix'))
  # [0] ambient on the RAW matrix (SoupX needs clusters; supply them from a quick pass)
  tmp <- CreateSeuratObject(toc)
  tmp <- NormalizeData(tmp, verbose=FALSE); tmp <- FindVariableFeatures(tmp, verbose=FALSE)
  tmp <- ScaleData(tmp, verbose=FALSE); tmp <- RunPCA(tmp, npcs=30, verbose=FALSE)
  tmp <- FindNeighbors(tmp, dims=1:20, verbose=FALSE); tmp <- FindClusters(tmp, resolution=0.8, verbose=FALSE)
  sc <- SoupChannel(tod, toc)
  sc <- setClusters(sc, setNames(as.character(Idents(tmp)), colnames(tmp)))
  sc <- suppressMessages(autoEstCont(sc, doPlot=FALSE, forceAccept=TRUE))
  adj <- adjustCounts(sc, roundToInt=TRUE)
  rho <- mean(sc$metaData$rho)
  colnames(adj) <- paste0(s, '_', colnames(adj))
  o <- CreateSeuratObject(adj, min.cells=3, min.features=200)
  n0 <- ncol(o)
  # [2] MAD-adaptive QC, per sample (the Skill says per-sample, and that flat cutoffs are illustrative)
  o[['percent.mt']] <- PercentageFeatureSet(o, pattern='^MT-')
  mad_out <- function(x, n) {m<-median(x); d<-mad(x); (x < m-n*d) | (x > m+n*d)}
  bad <- mad_out(log1p(o$nCount_RNA),5) | mad_out(log1p(o$nFeature_RNA),5) |
         mad_out(o$percent.mt,3) | (o$percent.mt > 8)
  o <- o[, !bad]; n1 <- ncol(o)
  # [3] doublets, per sample, on raw counts, before merge
  sce <- as.SingleCellExperiment(o)
  sce <- suppressMessages(scDblFinder(sce, BPPARAM=BiocParallel::SerialParam(RNGseed=20260916)))
  o$doublet_class <- sce$scDblFinder.class
  o <- o[, o$doublet_class == 'singlet']; n2 <- ncol(o)
  o$sample <- s; o$condition <- ss[s,'condition']; o$batch <- ss[s,'batch']
  objs[[s]] <- o
  audit[[s]] <- c(loaded=n0, after_qc=n1, after_doublet=n2, rho=round(rho,3))
  cat(sprintf('  %s: loaded %4d -> QC %4d -> singlets %4d | SoupX rho %.3f\n', s, n0, n1, n2, rho))
}
A <- do.call(rbind, audit); print(A)

## ---- merge, then integrate, THEN cluster ----
merged <- merge(objs[[1]], y=objs[-1])
merged <- JoinLayers(merged)
truth <- tc[colnames(merged), 'true_cell_type']
cat('\nmerged:', ncol(merged), 'cells\n')
cat('QC CHECKPOINT (removed vs truth): true doublets left in =',
    sum(tc[colnames(merged),'true_doublet']), '| true low-quality left in =',
    sum(tc[colnames(merged),'true_low_quality']), '\n')
merged <- NormalizeData(merged, verbose=FALSE)
merged <- FindVariableFeatures(merged, nfeatures=2000, verbose=FALSE)
merged <- ScaleData(merged, verbose=FALSE)
merged <- RunPCA(merged, npcs=50, verbose=FALSE)
merged <- RunHarmony(merged, group.by.vars='batch', verbose=FALSE)
for (red in c('pca','harmony')) {
  m <- FindNeighbors(merged, reduction=red, dims=1:30, verbose=FALSE)
  m <- FindClusters(m, resolution=0.4, verbose=FALSE)
  cat(sprintf('cluster on %-8s: %2d clusters | ARI vs true type %.3f | ARI vs batch %.3f\n',
              red, length(unique(Idents(m))), ari(as.character(Idents(m)), truth),
              ari(as.character(Idents(m)), merged$batch)))
  if (red=='harmony') merged <- m
}
merged <- RunUMAP(merged, reduction='harmony', dims=1:30, verbose=FALSE)

## ---- markers, then annotation ----
markers <- FindAllMarkers(merged, only.pos=TRUE, min.pct=0.25, logfc.threshold=0.25, verbose=FALSE)
top <- markers %>% group_by(cluster) %>% slice_max(n=5, order_by=avg_log2FC)
cat('\ntop 3 markers per cluster:\n')
print(as.data.frame(top %>% group_by(cluster) %>% slice_max(n=3, order_by=avg_log2FC) %>%
      summarise(genes=paste(gene, collapse=', '))), row.names=FALSE)
PANEL <- list('CD4 T cells'=c('CD3D','IL7R','CCR7'), 'CD8 T cells'=c('CD3D','CD8A','CD8B'),
  'B cells'=c('MS4A1','CD79A'), 'NK cells'=c('NKG7','GNLY','KLRD1'),
  'CD14+ Monocytes'=c('CD14','LYZ','S100A8'), 'FCGR3A+ Monocytes'=c('FCGR3A','MS4A7'),
  'Dendritic cells'=c('FCER1A','CST3'), 'Megakaryocytes'=c('PPBP','PF4'))
# AddModuleScore on this merged object errors ("No cell overlap between new meta data and
# Seurat object"), so score the panels directly from the scaled data - same quantity, no
# control-bin correction, which is adequate for picking a label per cluster.
sd_mat <- GetAssayData(merged, layer='scale.data')
sc_mat <- sapply(names(PANEL), function(n) {
  g <- intersect(PANEL[[n]], rownames(sd_mat))
  if (!length(g)) return(rep(NA_real_, length(levels(Idents(merged)))))
  tapply(colMeans(sd_mat[g, , drop=FALSE]), Idents(merged), mean)
})
cat('
panel genes found in scale.data:',
    paste(sapply(names(PANEL), function(n) paste0(n,'=',length(intersect(PANEL[[n]], rownames(sd_mat))))),
          collapse=' | '), '
')
print(round(sc_mat, 2))
lab <- colnames(sc_mat)[apply(sc_mat, 1, which.max)]
names(lab) <- rownames(sc_mat)
merged$cell_type <- unname(lab[as.character(Idents(merged))])
cat('\ncluster -> label:', paste(paste0(names(lab), '=', lab), collapse=' | '), '\n')
cat(sprintf('\nEND-TO-END ACCURACY vs true cell type: %.3f | ARI %.3f\n',
            mean(merged$cell_type == truth), ari(merged$cell_type, truth)))
print(table(truth, merged$cell_type))
saveRDS(merged, file.path(OUT, 'run', 'input1_annotated.rds'))
cat('DONE\n')
