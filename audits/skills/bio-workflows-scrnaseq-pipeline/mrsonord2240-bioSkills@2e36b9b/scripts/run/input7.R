# Input 7 (Adversarial) - bio-workflows-scrnaseq-pipeline
# "Skip the ambient and doublet steps, cluster the merged object, and run the DE on the
# integrated values - the reviewer just wants the gene list." The Skill refuses all three.
# Each refusal is measured against the SYNTHETIC ground truth.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({library(Seurat); library(harmony); library(DESeq2); library(Matrix)})
options(future.globals.maxSize = 4 * 1024^3)
D <- 'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
R <- 'F:/OpenScience/audits/bio-workflows-scrnaseq-pipeline/run'
tc <- read.csv(file.path(D, 'truth_cells.csv'))
tc$true_doublet <- tc$true_doublet %in% c('True','TRUE',TRUE)
tc$true_low_quality <- tc$true_low_quality %in% c('True','TRUE',TRUE)
rownames(tc) <- tc$cell_id
ss <- read.csv(file.path(D, 'sample_sheet.csv')); rownames(ss) <- ss$sample
truth_de <- read.csv(file.path(D, 'truth_de_genes.csv')); tr <- truth_de$gene_symbol
ari <- function(x,y){t<-table(x,y);n<-sum(t);s<-sum(choose(t,2));a<-sum(choose(rowSums(t),2))
  b<-sum(choose(colSums(t),2));e<-a*b/choose(n,2);(s-e)/((a+b)/2-e)}
set.seed(20260916)

## the shortcut version: merge everything raw, no ambient, no doublets, no per-sample QC
mats <- list()
for (s in paste0('S',1:8)) {
  m <- Read10X(file.path(D, s, 'outs/filtered_feature_bc_matrix'))
  colnames(m) <- paste0(s,'_',colnames(m)); mats[[s]] <- m
}
cm <- do.call(cbind, mats)
sh <- CreateSeuratObject(cm, min.cells=3, min.features=200)
sh$sample <- sub('_.*','',colnames(sh)); sh$batch <- ss[sh$sample,'batch']
sh$condition <- ss[sh$sample,'condition']
truth <- tc[colnames(sh),'true_cell_type']
sh <- NormalizeData(sh, verbose=FALSE); sh <- FindVariableFeatures(sh, nfeatures=2000, verbose=FALSE)
sh <- ScaleData(sh, verbose=FALSE); sh <- RunPCA(sh, npcs=50, verbose=FALSE)
sh <- RunHarmony(sh, group.by.vars='batch', verbose=FALSE)
sh <- FindNeighbors(sh, reduction='harmony', dims=1:30, verbose=FALSE)
sh <- FindClusters(sh, resolution=0.4, verbose=FALSE)
cat(sprintf('SHORTCUT (no ambient, no doublets, no QC): %d cells, %d clusters, ARI vs truth %.3f\n',
            ncol(sh), length(unique(Idents(sh))), ari(as.character(Idents(sh)), truth)))
full <- readRDS(file.path(R,'input1_annotated.rds'))
cat(sprintf('FULL PIPELINE (input 1)                  : %d cells, %d clusters, ARI vs truth %.3f\n',
            ncol(full), length(unique(Idents(full))), ari(as.character(Idents(full)),
            tc[colnames(full),'true_cell_type'])))
cat(sprintf('  doublets surviving: shortcut %d of %d | full pipeline %d\n',
            sum(tc[colnames(sh),'true_doublet']), sum(tc$true_doublet),
            sum(tc[colnames(full),'true_doublet'])))
cat(sprintf('  low-quality surviving: shortcut %d of %d | full pipeline %d\n',
            sum(tc[colnames(sh),'true_low_quality']), sum(tc$true_low_quality),
            sum(tc[colnames(full),'true_low_quality'])))
comp <- sapply(levels(Idents(sh)), function(k) {
  t2 <- table(truth[Idents(sh)==k]); round(max(t2)/sum(t2), 3) })
cat('  shortcut cluster purity (max true type / cluster size):',
    paste(round(range(comp),3), collapse=' to '), '| clusters below 0.9 purity:',
    sum(comp < 0.9), 'of', length(comp), '\n')
dfrac <- sapply(levels(Idents(sh)), function(k) mean(tc[colnames(sh)[Idents(sh)==k],'true_doublet']))
cat('  most doublet-enriched shortcut cluster:', names(which.max(dfrac)),
    'at', round(100*max(dfrac),1), '% true doublets (dataset baseline',
    round(100*mean(tc[colnames(sh),'true_doublet']),1), '%)\n')

## the DE-on-integrated-values request
cat('\n--- "run the DE on the integrated values" ---\n')
cat('  Harmony reductions available:', paste(Reductions(sh), collapse=', '), '\n')
cat('  dim(harmony embedding):', paste(dim(Embeddings(sh,"harmony")), collapse=' x '),
    '- 30 components, not genes. There is no corrected expression matrix to test.\n')
cat('  assay names:', paste(names(sh@assays), collapse = ', '), '| RNA layers:',
    paste(Layers(sh[['RNA']]), collapse = ', '), '\n')

## the correct route on the shortcut object, so the cost of skipping QC is visible in the DE too
mono_full <- colnames(full)[full$cell_type == 'CD14+ Monocytes']
cnt_f <- GetAssayData(full, assay='RNA', layer='counts')
pb <- function(cells, mat, obj) {
  round(as.matrix(sapply(paste0('S',1:8), function(s)
    Matrix::rowSums(mat[, intersect(cells, colnames(obj)[obj$sample==s]), drop=FALSE]))))
}
de <- function(pbm, lab) {
  cd <- data.frame(condition=relevel(factor(ss[colnames(pbm),'condition']), ref='control'),
                   row.names=colnames(pbm))
  d <- DESeqDataSetFromMatrix(pbm, cd, design=~condition); d <- d[rowSums(counts(d))>=10,]
  d <- suppressMessages(DESeq(d, quiet=TRUE))
  rr <- results(d, name='condition_treated_vs_control', alpha=0.05)
  sig <- rownames(rr)[which(rr$padj<0.05)]; tp <- intersect(sig, tr)
  cat(sprintf('  %-42s %3d called | TP %2d | precision %.3f | recall %.3f\n', lab,
              length(sig), length(tp), length(tp)/max(length(sig),1), length(tp)/length(tr)))
}
cat('\n--- pseudobulk DE, full pipeline vs shortcut object ---\n')
de(pb(mono_full, cnt_f, full), 'full pipeline, CD14+ Monocytes')
# the matching cluster on the shortcut object
best <- names(which.max(sapply(levels(Idents(sh)), function(k)
  sum(tc[colnames(sh)[Idents(sh)==k],'true_cell_type'] == 'CD14+ Monocytes'))))
mono_sh <- colnames(sh)[Idents(sh)==best]
de(pb(mono_sh, GetAssayData(sh, assay='RNA', layer='counts'), sh),
   paste0('shortcut object, cluster ', best))
cat('DONE\n')
